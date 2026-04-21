<template>
  <div class="page-runblade-price">
    <!-- 顶部操作栏 -->
    <el-card shadow="never" class="header-card">
      <div class="header-bar">
        <h3>三角洲跑刀跑手价格台账</h3>
        <div class="action-btns">
          <el-button type="success" icon="el-icon-upload2" @click="handleImport">批量导入</el-button>
          <el-button type="primary" icon="el-icon-download" @click="handleExport">导出Excel</el-button>
          <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增价格</el-button>
        </div>
      </div>
    </el-card>

    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="业务类型">
          <el-select v-model="searchForm.business_type" placeholder="请选择业务类型" clearable style="width: 150px">
            <el-option
              v-for="item in businessTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物品格子">
          <el-select v-model="searchForm.grid_type" placeholder="请选择物品格子" clearable style="width: 150px">
            <el-option
              v-for="item in gridTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="备注说明"
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
        <el-table-column prop="business_type" label="业务类型" width="120" align="center">
          <template slot-scope="{ row }">
            <el-tag :type="row.business_type === '跑刀' ? 'success' : 'warning'" size="mini">
              {{ row.business_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="grid_type" label="物品格子" width="120" align="center">
          <template slot-scope="{ row }">
            <el-tag type="info" size="mini">{{ row.grid_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="unit_price" label="单人单价(R)" width="130" align="center" />
        <el-table-column prop="rmb" label="人民币R" width="120" align="right">
          <template slot-scope="{ row }">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ row.rmb | formatMoney }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="game_money" label="对应游戏币" width="130" align="center" />
        <el-table-column prop="remark" label="备注说明" min-width="180" show-overflow-tooltip />
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
        <el-form-item label="业务类型" prop="business_type">
          <el-select v-model="form.business_type" placeholder="请选择业务类型" style="width: 100%">
            <el-option
              v-for="item in businessTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物品格子" prop="grid_type">
          <el-select v-model="form.grid_type" placeholder="请选择物品格子" style="width: 100%">
            <el-option
              v-for="item in gridTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="单人单价(R)" prop="unit_price">
          <el-input v-model="form.unit_price" placeholder="请输入单人单价" />
        </el-form-item>
        <el-form-item label="人民币R" prop="rmb">
          <el-input-number v-model="form.rmb" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="对应游戏币" prop="game_money">
          <el-input v-model="form.game_money" placeholder="请输入对应游戏币" />
        </el-form-item>
        <el-form-item label="备注说明" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注说明" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </div>
    </el-dialog>

    <!-- 批量导入弹窗 -->
    <el-dialog
      title="批量导入跑刀跑手价格"
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
          表头：业务类型、物品格子、单人单价(R)、人民币R、对应游戏币、备注说明<br/>
          <span style="color: #f56c6c;">业务类型必填：跑刀/跑手；物品格子必填：9格/6格/4格/2格/4-6格</span>
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
  getRunBladePriceList,
  createRunBladePrice,
  updateRunBladePrice,
  deleteRunBladePrice,
  exportExcel,
  importExcel,
} from '@/api/runbladeprice/runbladeprice'

export default {
  name: 'RunBladePrice',
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
        business_type: '',
        grid_type: '',
        search: '',
      },
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0,
      },
      dialogVisible: false,
      dialogTitle: '新增价格',
      submitting: false,
      form: {
        id: null,
        business_type: '',
        grid_type: '',
        unit_price: '',
        rmb: 0,
        game_money: '',
        remark: '',
      },
      rules: {
        business_type: [{ required: true, message: '请选择业务类型', trigger: 'change' }],
        grid_type: [{ required: true, message: '请选择物品格子', trigger: 'change' }],
      },
      importDialogVisible: false,
      importing: false,
      uploadFile: null,
      businessTypeOptions: [
        { value: '跑刀', label: '跑刀' },
        { value: '跑手', label: '跑手' },
      ],
      gridTypeOptions: [
        { value: '9格', label: '9格' },
        { value: '6格', label: '6格' },
        { value: '4格', label: '4格' },
        { value: '2格', label: '2格' },
        { value: '4-6格', label: '4-6格' },
      ],
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
          business_type: this.searchForm.business_type || undefined,
          grid_type: this.searchForm.grid_type || undefined,
        }
        const res = await getRunBladePriceList(params)
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
      this.searchForm = { business_type: '', grid_type: '', search: '' }
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
      this.dialogTitle = '新增价格'
      this.form = {
        id: null,
        business_type: '',
        grid_type: '',
        unit_price: '',
        rmb: 0,
        game_money: '',
        remark: '',
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogTitle = '编辑价格'
      this.form = { ...row }
      this.dialogVisible = true
    },

    async handleDelete(row) {
      this.$confirm(`确定要删除 "${row.business_type}-${row.grid_type}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          await deleteRunBladePrice(row.id)
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
            await updateRunBladePrice(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createRunBladePrice(this.form)
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
.page-runblade-price {
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
