<template>
  <div class="page-escort-price">
    <!-- 顶部操作栏 -->
    <el-card shadow="never" class="header-card">
      <div class="header-bar">
        <h3>三角洲护航价格台账</h3>
        <div class="action-btns">
          <el-button type="success" icon="el-icon-upload2" @click="handleImport">批量导入</el-button>
          <el-button type="primary" icon="el-icon-download" @click="handleExport">导出Excel</el-button>
          <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增护航</el-button>
        </div>
      </div>
    </el-card>

    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="套餐类型">
          <el-select v-model="searchForm.package_type" placeholder="请选择套餐类型" clearable style="width: 180px">
            <el-option
              v-for="item in packageTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="套餐名称/备注"
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
        <el-table-column prop="package_type" label="套餐类型" width="140" align="center">
          <template slot-scope="{ row }">
            <el-tag :type="getPackageTypeTag(row.package_type)" size="mini">
              {{ row.package_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="package_name" label="套餐名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="sell_price" label="出售价格(R)" width="120" align="right">
          <template slot-scope="{ row }">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ row.sell_price | formatMoney }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="guarantee_money" label="保底游戏币(w)" width="130" align="right">
          <template slot-scope="{ row }">{{ row.guarantee_money | formatMoney }}w</template>
        </el-table-column>
        <el-table-column prop="bomb_extra" label="炸单额外加(w)" width="130" align="right">
          <template slot-scope="{ row }">+{{ row.bomb_extra | formatMoney }}w</template>
        </el-table-column>
        <el-table-column prop="game_times" label="对局场次" width="100" align="center" />
        <el-table-column prop="remark" label="套餐备注" min-width="150" show-overflow-tooltip />
        <el-table-column prop="create_datetime" label="创建时间" width="160" />
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
      width="650px"
      @close="handleDialogClose"
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="120px" size="small">
        <el-form-item label="套餐类型" prop="package_type">
          <el-select v-model="form.package_type" placeholder="请选择套餐类型" style="width: 100%">
            <el-option
              v-for="item in packageTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="套餐名称" prop="package_name">
          <el-input v-model="form.package_name" placeholder="请输入套餐名称" />
        </el-form-item>
        <el-form-item label="出售价格(R)" prop="sell_price">
          <el-input-number v-model="form.sell_price" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="保底游戏币(w)" prop="guarantee_money">
          <el-input-number v-model="form.guarantee_money" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="炸单额外加(w)" prop="bomb_extra">
          <el-input-number v-model="form.bomb_extra" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="对局场次" prop="game_times">
          <el-input v-model="form.game_times" placeholder="请输入对局场次" />
        </el-form-item>
        <el-form-item label="套餐备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入套餐备注" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </div>
    </el-dialog>

    <!-- 批量导入弹窗 -->
    <el-dialog
      title="批量导入护航价格"
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
          支持 .xlsx / .xls 格式<br/>
          表头：套餐类型、套餐名称、出售价格(R)、保底游戏币(w)、炸单额外加(w)、对局场次、备注<br/>
          <span style="color: #f56c6c;">套餐类型必填：体验单/绝密监狱航天/绝密巴克什/赌约单</span>
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
  getEscortPriceList,
  createEscortPrice,
  updateEscortPrice,
  deleteEscortPrice,
  exportExcel,
  importExcel,
} from '@/api/escortprice/escortprice'

export default {
  name: 'EscortPrice',
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
        package_type: '',
        search: '',
      },
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0,
      },
      dialogVisible: false,
      dialogTitle: '新增护航',
      submitting: false,
      form: {
        id: null,
        package_type: '',
        package_name: '',
        sell_price: 0,
        guarantee_money: 0,
        bomb_extra: 0,
        game_times: '',
        remark: '',
      },
      rules: {
        package_type: [{ required: true, message: '请选择套餐类型', trigger: 'change' }],
        package_name: [{ required: true, message: '请输入套餐名称', trigger: 'blur' }],
      },
      importDialogVisible: false,
      importing: false,
      uploadFile: null,
      packageTypeOptions: [
        { value: '体验单', label: '体验单' },
        { value: '绝密监狱航天', label: '绝密监狱航天' },
        { value: '绝密巴克什', label: '绝密巴克什' },
        { value: '赌约单', label: '赌约单' },
      ],
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    getPackageTypeTag(type) {
      const typeMap = {
        '体验单': 'info',
        '绝密监狱航天': 'danger',
        '绝密巴克什': 'warning',
        '赌约单': 'success',
      }
      return typeMap[type] || ''
    },
    async fetchData() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.currentPage,
          limit: this.pagination.pageSize,
          search: this.searchForm.search || undefined,
          package_type: this.searchForm.package_type || undefined,
        }
        const res = await getEscortPriceList(params)
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
      this.searchForm = { package_type: '', search: '' }
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
      this.dialogTitle = '新增护航'
      this.form = {
        id: null,
        package_type: '',
        package_name: '',
        sell_price: 0,
        guarantee_money: 0,
        bomb_extra: 0,
        game_times: '',
        remark: '',
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogTitle = '编辑护航'
      this.form = { ...row }
      this.dialogVisible = true
    },

    async handleDelete(row) {
      this.$confirm(`确定要删除 "${row.package_type}-${row.package_name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          await deleteEscortPrice(row.id)
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
            await updateEscortPrice(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createEscortPrice(this.form)
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
.page-escort-price {
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
