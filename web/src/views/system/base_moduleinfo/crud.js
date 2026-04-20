import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    rowHandle: {
      view: {
        disabled () {
          // return !vm.hasPermissions('Retrieve')
          return false
        }
      },
      edit: {
        disabled () {
          // return !vm.hasPermissions('Update')
          return false
        }
      },
      remove: {
        disabled () {
          // return !vm.hasPermissions('Delete')
          return false
        }
      },
      fixed: 'right'
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    formOptions: { // 表单宽度
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    indexRow: { // 序号
      title: '序号',
      align: 'center',
      width: 60
    },
    selectionRow: { // 多选框
      align: 'center',
      width: 46
    },
    columns: [
      {
        title: 'Id',
        key: 'id',
        form: { // 表单配置
          disabled: true // 禁用表单编辑
        },
        // type: 'select',
        // dict: { url: ''}, //数据字典
        // search: { disabled: false }, // 开启查询
        disabled: true, // 隐藏列
        sortable: true
      },
      {
        title: '所属项目',
        key: 'project_belong',
        type: 'select',
        dict: {
          // cache: false, 默认 读缓存信息 true
          cache: false, // 每次都访问一次数据库
          url: '/base/projectInfo/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'project_name' // 数据字典中label字段的属性名
        },
        // search: { disabled: false }, // 开启查询
        // disabled: true, // 隐藏列
        form: { // 表单配置
          disabled: false, // 禁用表单编辑
          rules: [{ required: true, message: '' }],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        sortable: true
      },
      {
        title: '模块名称',
        key: 'module_name',
        // type: 'select',
        // dict: { url: ''}, //数据字典
        search: { disabled: false }, // 开启查询
        // disabled: true, // 隐藏列
        form: { // 表单配置
          disabled: false, // 禁用表单编辑
          rules: [{ required: true, message: '模块名称' }],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入模块名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        sortable: true
      },
      {
        title: '负责人',
        key: 'test_user',
        search: {
          disabled: true
        },
        type: 'table-selector',
        dict: {
          cache: false,
          url: '/api/system/user/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, {
            form,
            component
          }) => {
            return request({
              url: url,
              params: {
                page: 1,
                limit: 10
              }
            }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            pagination: true,
            props: { multiple: true },
            elProps: {
              columns: [
                {
                  field: 'name',
                  title: '用户名'
                },
                {
                  field: 'mobile',
                  title: '手机号'
                }
              ]
            }
          }
        }
      }

    ].concat(vm.commonEndColumns())
  }
}
