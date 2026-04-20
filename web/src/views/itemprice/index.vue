<template>
  <div class="page-item-price">
    <!-- 顶部操作栏 -->
    <el-card shadow="never" class="header-card">
      <div class="header-bar">
        <h3>物品价格台账</h3>
        <div class="action-btns">
          <el-button type="success" icon="el-icon-upload2" @click="handleImport">批量导入</el-button>
          <el-button type="primary" icon="el-icon-download" @click="handleExport">导出Excel</el-button>
          <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增物品</el-button>
        </div>
      </div>
    </el-card>

    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="物资名称/备注"
            clearable
            @keyup.enter.native="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        size="small"
        max-height="600"
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="item_name" label="物资名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="reference_price" label="参考价格" width="120" align="right">
          <template slot-scope="{ row }">{{ row.reference_price | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="out_price" label="出价格" width="120" align="right">
          <template slot-scope="{ row }">
            <span :style="{ color: row.out_price >= 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ row.out_price | formatMoney }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="item_remark" label="物品备注规格" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template slot-scope="{ row }">
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleEdit(row)" />
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(row)" />
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        class="pagination"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        :current-page="pagination.currentPage"
        :total="pagination.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px" size="small">
        <el-form-item label="物资名称" prop="item_name">
          <el-input v-model="form.item_name" placeholder="请输入物资名称" />
        </el-form-item>
        <el-form-item label="参考价格" prop="reference_price">
          <el-input-number v-model="form.reference_price" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="出价格" prop="out_price">
          <el-input-number v-model="form.out_price" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="物品备注规格" prop="item_remark">
          <el-input v-model="form.item_remark" type="textarea" :rows="3" placeholder="请输入物品规格备注" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </div>
    </el-dialog>

    <!-- 批量导入弹窗 -->
    <el-dialog
      title="批量导入物品价格"
      :visible.sync="importDialogVisible"
      width="500px"
    >
      <el-upload
        ref="upload"
        class="upload-demo"
        drag
        action=""
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".xlsx,.xls"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将Excel文件拖到此处，或<em>点击上传</em></div>
        <div slot="tip" class="el-upload__tip">
          支持 .xlsx / .xls 格式，表头：物资名称、参考价格、出价格、物品备注规格
        </div>
      </el-upload>
      <div slot="footer">
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importing" @click="handleImportSubmit">开始导入</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getItemPriceList,
  createItemPrice,
  updateItemPrice,
  deleteItemPrice,
  exportExcel,
  importExcel,
} from '@/api/itemprice/itemprice'

export default {
  name: 'ItemPrice',
  filters: {
    formatMoney(val) {
      if (val === null || val === undefined) return '0.00'
      return Number(val).toFixed(2)
    },
  },
  data() {
    return {
      loading: false,
      tableData: [],
      searchForm: {
        search: '',
      },
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0,
      },
      dialogVisible: false,
      dialogTitle: '新增物品',
      submitting: false,
      form: {
        id: null,
        item_name: '',
        reference_price: 0,
        out_price: 0,
        item_remark: '',
      },
      rules: {
        item_name: [{ required: true, message: '请输入物资名称', trigger: 'blur' }],
      },
      importDialogVisible: false,
      importing: false,
      uploadFile: null,
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.currentPage,
          limit: this.pagination.pageSize,
          search: this.searchForm.search || undefined,
        }
        const res = await getItemPriceList(params)
        if (res && res.data) {
          const pageData = res.data
          if (pageData.data && Array.isArray(pageData.data)) {
            this.tableData = pageData.data
            this.pagination.total = pageData.total || 0
          }
        }
      } catch (error) {
        this.$message.error('获取数据失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },

    handleSearch() {
      this.pagination.currentPage = 1
      this.fetchData()
    },

    handleReset() {
      this.searchForm = { search: '' }
      this.pagination.currentPage = 1
      this.fetchData()
    },

    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.fetchData()
    },

    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.fetchData()
    },

    handleAdd() {
      this.dialogTitle = '新增物品'
      this.form = {
        id: null,
        item_name: '',
        reference_price: 0,
        out_price: 0,
        item_remark: '',
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogTitle = '编辑物品'
      this.form = { ...row }
      this.dialogVisible = true
    },

    async handleDelete(row) {
      this.$confirm(`确定要删除 "${row.item_name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          await deleteItemPrice(row.id)
          this.$message.success('删除成功')
          this.fetchData()
        } catch (error) {
          this.$message.error('删除失败: ' + error.message)
        }
      })
    },

    async handleSubmit() {
      this.$refs.form.validate(async (valid) => {
        if (!valid) return
        this.submitting = true
        try {
          if (this.form.id) {
            await updateItemPrice(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createItemPrice(this.form)
            this.$message.success('创建成功')
          }
          this.dialogVisible = false
          this.fetchData()
        } catch (error) {
          this.$message.error('操作失败: ' + error.message)
        } finally {
          this.submitting = false
        }
      })
    },

    handleDialogClose() {
      this.$refs.form && this.$refs.form.resetFields()
    },

    handleExport() {
      exportExcel()
    },

    handleImport() {
      this.uploadFile = null
      this.importDialogVisible = true
    },

    handleFileChange(file) {
      this.uploadFile = file.raw
    },

    async handleImportSubmit() {
      if (!this.uploadFile) {
        this.$message.warning('请选择Excel文件')
        return
      }
      this.importing = true
      try {
        const res = await importExcel(this.uploadFile)
        this.$message.success(res.msg || '导入成功')
        this.importDialogVisible = false
        this.fetchData()
      } catch (error) {
        this.$message.error('导入失败: ' + error.message)
      } finally {
        this.importing = false
      }
    },
  },
}
</script>

<style scoped lang="scss">
.page-item-price {
  padding: 10px;

  .header-card {
    margin-bottom: 15px;

    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h3 {
        margin: 0;
        font-size: 18px;
      }

      .action-btns {
        display: flex;
        gap: 10px;
      }
    }
  }

  .search-card {
    margin-bottom: 15px;
  }

  .pagination {
    margin-top: 15px;
    text-align: right;
  }
}
</style>
