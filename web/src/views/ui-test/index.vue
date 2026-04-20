<template>
  <d2-container class="page-business">
    <template slot="header">
      <div class="header-bar">
        <h3>业务数据登记</h3>
        <el-button type="success" icon="el-icon-download" @click="handleExport">导出Excel</el-button>
      </div>
    </template>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card green">
          <div class="stat-title">总盈余</div>
          <div class="stat-value">{{ stats.total_profit_all || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card red">
          <div class="stat-title">平台总扣除</div>
          <div class="stat-value">{{ stats.total_platform_deduct || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card orange">
          <div class="stat-title">成本总</div>
          <div class="stat-value">{{ stats.total_cost_all || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card blue">
          <div class="stat-title">月总盈余</div>
          <div class="stat-value">{{ stats.monthly_profit_total || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card cyan">
          <div class="stat-title">月平台总扣除</div>
          <div class="stat-value">{{ stats.monthly_platform_deduct || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="stat-card pink">
          <div class="stat-title">月成本总</div>
          <div class="stat-value">{{ stats.monthly_cost_total || 0 | formatMoney }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 按月汇总 -->
    <el-card class="monthly-card" shadow="never">
      <div slot="header">
        <span>按月汇总</span>
        <el-button
          style="float: right; padding: 3px 10px"
          type="text"
          @click="fetchMonthlyData"
        >刷新</el-button>
      </div>
      <el-table :data="monthlyData" stripe size="mini" max-height="200">
        <el-table-column prop="month" label="月份" width="120" />
        <el-table-column prop="count" label="笔数" width="80" align="center" />
        <el-table-column prop="total_receipt" label="月流水" width="120" align="right">
          <template slot-scope="{ row }">{{ row.total_receipt || 0 | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="total_profit" label="月盈余" width="120" align="right">
          <template slot-scope="{ row }">{{ row.total_profit || 0 | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="total_platform_deduct" label="月平台扣除" width="130" align="right">
          <template slot-scope="{ row }">{{ row.total_platform_deduct || 0 | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="total_cost_deduct" label="月成本" width="120" align="right">
          <template slot-scope="{ row }">{{ row.total_cost_deduct || 0 | formatMoney }}</template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 搜索 -->
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="searchForm" size="small">
        <el-form-item label="微信号">
          <el-input v-model="searchForm.wechat_id" placeholder="请输入微信号" clearable />
        </el-form-item>
        <el-form-item label="撞车平台">
          <el-input v-model="searchForm.collision_platform" placeholder="请输入撞车平台" clearable />
        </el-form-item>
        <el-form-item label="出货平台">
          <el-input v-model="searchForm.shipment_platform" placeholder="请输入出货平台" clearable />
        </el-form-item>
        <el-form-item label="是否付款">
          <el-select v-model="searchForm.is_paid" placeholder="请选择" clearable>
            <el-option label="已付款" :value="true" />
            <el-option label="未付款" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="业务日期">
          <el-date-picker
            v-model="searchForm.record_date"
            type="date"
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据列表 -->
    <el-card shadow="never">
      <div slot="header">
        <span>数据列表</span>
        <el-button
          style="float: right; padding: 3px 10px"
          type="primary"
          icon="el-icon-plus"
          @click="handleAdd"
        >新增</el-button>
      </div>
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        size="small"
        max-height="500"
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="wechat_id" label="微信号" width="100" show-overflow-tooltip />
        <el-table-column prop="demand" label="需求" width="150" show-overflow-tooltip />
        <el-table-column prop="quantity" label="数量" width="70" align="center" />
        <el-table-column prop="contact" label="联系方式" width="120" show-overflow-tooltip />
        <el-table-column prop="collision_platform" label="撞车平台" width="100" show-overflow-tooltip />
        <el-table-column prop="shipment_platform" label="出货平台" width="100" show-overflow-tooltip />
        <el-table-column prop="payment_method" label="付款方式" width="100" show-overflow-tooltip />
        <el-table-column prop="is_paid" label="付款" width="70" align="center">
          <template slot-scope="{ row }">
            <el-tag :type="row.is_paid ? 'success' : 'danger'" size="mini">
              {{ row.is_paid ? '已付' : '未付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price_payable" label="应付" width="90" align="right">
          <template slot-scope="{ row }">{{ row.price_payable | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="price_actual" label="实付" width="90" align="right">
          <template slot-scope="{ row }">{{ row.price_actual | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="platform_deduct" label="平台扣除" width="100" align="right">
          <template slot-scope="{ row }">{{ row.platform_deduct | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="cost_deduct" label="成本扣除" width="100" align="right">
          <template slot-scope="{ row }">{{ row.cost_deduct | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="redpacket" label="红包" width="80" align="right">
          <template slot-scope="{ row }">{{ row.redpacket | formatMoney }}</template>
        </el-table-column>
        <el-table-column prop="profit" label="盈余" width="90" align="right">
          <template slot-scope="{ row }">
            <span :style="{ color: row.profit >= 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ row.profit | formatMoney }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="record_date" label="业务日期" width="110" />
        <el-table-column label="操作" width="150" fixed="right" align="center">
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
      width="900px"
      @close="handleDialogClose"
    >
      <el-form ref="form" :model="form" label-width="110px" size="small">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="微信号">
              <el-input v-model="form.wechat_id" placeholder="请输入微信号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="业务日期">
              <el-date-picker
                v-model="form.record_date"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="需求">
              <el-input v-model="form.demand" placeholder="请输入需求" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数量">
              <el-input-number v-model="form.quantity" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系方式">
              <el-input v-model="form.contact" placeholder="请输入联系方式" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款方式">
              <el-input v-model="form.payment_method" placeholder="请输入付款方式" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="撞车平台">
              <el-input v-model="form.collision_platform" placeholder="请输入撞车平台" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出货平台">
              <el-input v-model="form.shipment_platform" placeholder="请输入出货平台" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="应付价格">
              <el-input-number v-model="form.price_payable" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="实付价格">
              <el-input-number v-model="form.price_actual" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="是否付款">
              <el-switch v-model="form.is_paid" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="平台扣除">
              <el-input-number v-model="form.platform_deduct" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="成本扣除">
              <el-input-number v-model="form.cost_deduct" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="红包">
              <el-input-number v-model="form.redpacket" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
  </d2-container>
</template>

<script>
import {
  getBusinessList,
  createBusiness,
  updateBusiness,
  deleteBusiness,
  getStats,
  getMonthlyList,
  exportExcel,
} from '@/api/uitest/business'

export default {
  name: 'BusinessRecord',
  filters: {
    formatMoney(val) {
      if (val === null || val === undefined) return '0.00'
      return Number(val).toFixed(2)
    },
  },
  data() {
    return {
      loading: false,
      submitting: false,
      tableData: [],
      monthlyData: [],
      stats: {
        total_profit_all: 0,
        total_platform_deduct: 0,
        total_cost_all: 0,
        monthly_profit_total: 0,
        monthly_platform_deduct: 0,
        monthly_cost_total: 0,
      },
      searchForm: {
        wechat_id: '',
        collision_platform: '',
        shipment_platform: '',
        is_paid: '',
        record_date: '',
      },
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0,
      },
      dialogVisible: false,
      dialogTitle: '新增业务数据',
      form: {
        id: null,
        wechat_id: '',
        demand: '',
        quantity: 0,
        contact: '',
        collision_platform: '',
        shipment_platform: '',
        payment_method: '',
        is_paid: false,
        price_payable: 0,
        price_actual: 0,
        platform_deduct: 0,
        cost_deduct: 0,
        redpacket: 0,
        remark: '',
        record_date: '',
      },
    }
  },
  mounted() {
    this.fetchData()
    this.fetchStats()
    this.fetchMonthlyData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.currentPage,
          limit: this.pagination.pageSize,
          ...this.searchForm,
        }
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) delete params[key]
        })
        const res = await getBusinessList(params)
        console.log('API返回:', res)
        // 处理分页响应格式 {code, msg, data: {page, total, limit, data: [...]}}
        if (res && res.data) {
          const pageData = res.data
          if (pageData.data && Array.isArray(pageData.data)) {
            this.tableData = pageData.data
            this.pagination.total = pageData.total || 0
          } else if (Array.isArray(pageData)) {
            this.tableData = pageData
            this.pagination.total = pageData.length
          } else {
            this.tableData = []
            this.pagination.total = 0
          }
        } else if (Array.isArray(res)) {
          this.tableData = res
          this.pagination.total = res.length
        }
      } catch (error) {
        this.$message.error('获取数据失败: ' + error.message)
        this.tableData = []
        this.pagination.total = 0
      } finally {
        this.loading = false
      }
    },

    async fetchStats() {
      try {
        const res = await getStats()
        console.log('=== 1. fetchStats res ===', res)
        
        // 后端分页包装：res.data = {page, limit, total, data: {...}}
        const resData = res.data
        const actualData = resData.data || resData
        
        console.log('=== 2. actualData ===', actualData)
        
        if (!actualData) return
        
        // 直接赋值
        this.stats.total_profit_all = Number(actualData.total_profit_all || 0)
        this.stats.total_platform_deduct = Number(actualData.total_platform_deduct || 0)
        this.stats.total_cost_all = Number(actualData.total_cost_all || 0)
        this.stats.monthly_profit_total = Number(actualData.monthly_profit_total || 0)
        this.stats.monthly_platform_deduct = Number(actualData.monthly_platform_deduct || 0)
        this.stats.monthly_cost_total = Number(actualData.monthly_cost_total || 0)
        
        console.log('=== 3. this.stats after update ===', this.stats)
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    },

    async fetchMonthlyData() {
      try {
        const res = await getMonthlyList()
        console.log('=== monthly_list res ===', JSON.stringify(res))
        
        // 后端分页包装：res.data = {page, limit, total, data: [...]}
        const resData = res.data
        if (resData.data && Array.isArray(resData.data)) {
          this.monthlyData = resData.data
        } else if (Array.isArray(resData)) {
          this.monthlyData = resData
        } else {
          this.monthlyData = []
        }
        
        console.log('=== monthlyData ===', this.monthlyData)
      } catch (error) {
        console.error('获取月度数据失败:', error)
      }
    },

    handleSearch() {
      this.pagination.currentPage = 1
      this.fetchData()
      this.fetchStats()
    },

    handleReset() {
      this.searchForm = {
        wechat_id: '',
        collision_platform: '',
        shipment_platform: '',
        is_paid: '',
        record_date: '',
      }
      this.pagination.currentPage = 1
      this.fetchData()
      this.fetchStats()
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
      this.dialogTitle = '新增业务数据'
      this.form = {
        id: null,
        wechat_id: '',
        demand: '',
        quantity: 0,
        contact: '',
        collision_platform: '',
        shipment_platform: '',
        payment_method: '',
        is_paid: false,
        price_payable: 0,
        price_actual: 0,
        platform_deduct: 0,
        cost_deduct: 0,
        redpacket: 0,
        remark: '',
        record_date: new Date().toISOString().split('T')[0],
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogTitle = '编辑业务数据'
      this.form = { ...row }
      this.dialogVisible = true
    },

    async handleDelete(row) {
      this.$confirm(`确定要删除微信号为 "${row.wechat_id}" 的记录吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          await deleteBusiness(row.id)
          this.$message.success('删除成功')
          this.fetchData()
          this.fetchStats()
          this.fetchMonthlyData()
        } catch (error) {
          this.$message.error('删除失败: ' + error.message)
        }
      })
    },

    async handleSubmit() {
      this.submitting = true
      try {
        if (this.form.id) {
          await updateBusiness(this.form.id, this.form)
          this.$message.success('更新成功')
        } else {
          await createBusiness(this.form)
          this.$message.success('创建成功')
        }
        this.dialogVisible = false
        this.fetchData()
        this.fetchStats()
        this.fetchMonthlyData()
      } catch (error) {
        this.$message.error('操作失败: ' + error.message)
      } finally {
        this.submitting = false
      }
    },

    handleDialogClose() {
      this.$refs.form && this.$refs.form.resetFields()
    },

    handleExport() {
      exportExcel()
    },
  },
}
</script>

<style scoped lang="scss">
.page-business {
  padding: 10px;

  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      font-size: 18px;
    }
  }

  .stats-row {
    margin-bottom: 15px;

    .stat-card {
      text-align: center;
      padding: 5px 0;

      .stat-title {
        font-size: 13px;
        color: #909399;
        margin-bottom: 8px;
      }

      .stat-value {
        font-size: 22px;
        font-weight: bold;
      }
    }

    .green .stat-value { color: #67c23a; }
    .red .stat-value { color: #f56c6c; }
    .orange .stat-value { color: #e6a23c; }
    .blue .stat-value { color: #409eff; }
    .cyan .stat-value { color: #13ce66; }
    .pink .stat-value { color: #ff69b4; }
  }

  .monthly-card {
    margin-bottom: 15px;
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
