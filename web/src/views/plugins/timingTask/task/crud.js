/*
 * @创建文件时间: 2021-08-22 09:45:19
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 22:11:49
 * 联系Qq:1638245306
 * @文件介绍:
 */
import { BUTTON_STATUS_NUMBER } from '@/config/button'
import { urlPrefix } from './api'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%'
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: '50%'
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },
    selectionRow: { // 多选框
      align: 'center',
      width: 46
    },
    rowHandle: {
      dropdown: { // 操作列折叠
        atLeast: 0, // 至少几个以上的按钮才会被折叠,注意show=false的按钮也会计算在内（行编辑按钮默认是隐藏的也会占一个位置）
        text: '更多', // dropdown按钮文字
        type: 'primary',
        icon: 'el-icon-more'
      },
      width: 150,
      view: {
        thin: true,
        text: '查看',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '修改',
        show: true
      },
      remove: {
        thin: true,
        text: '删除',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: [
        {
          thin: true,
          text: '测试结果',
          // size: 'small',
          icon: 'el-icon-s-data',
          disabled () {
            // return !vm.hasPermissions('Retrieve')
            return false
          },
          emit: 'toDetail'
        }
      ]
    },
    columns: [
      {
        title: '任务名称',
        key: 'name',
        sortable: true,
        search: {
          disabled: true
        },
        width: 120,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请填写任务名称！'
          }
        }
      },
      {
        title: 'CRON',
        key: 'crontab_str',
        sortable: true,
        rowSlot: true,
        width: 200,
        search: {
          disabled: true
        },
        type: 'cron-selector',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请填选择CRON！'
          }
        },
        component: {}
      },
      {
        title: '执行的任务',
        key: 'task',
        sortable: true,
        width: 400,
        search: {
          disabled: false
        },
        type: 'select',
        dict: {
          url: urlPrefix + 'job_list/'
        },
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请选择执行的任务！'
          }
        }
      },
      {
        title: '状态',
        key: 'enabled',
        search: {
          disabled: false
        },
        width: 140,
        type: 'switch',
        dict: {
          data: BUTTON_STATUS_NUMBER
        },
        form: {
          disabled: true,
          component: {
            span: 12
          }
        },
        component: {
          props: {
            'active-text': '启用',
            'inactive-text': '暂停'
          },
          disabled () {
            return !vm.hasPermissions('Update')
          },
          on: {
            change (event) { vm.onSwitchTask(event.scope) }
          }
        }
      },
      {
        title: '创建时间',
        key: 'date_changed',
        width: 160,
        search: {
          disabled: true
        },
        show: false,
        type: 'datetime',
        sortable: true,
        form: {
          disabled: true
        }
      },
      {
        title: '任务参数',
        key: 'kwargs',
        type: 'textarea',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '任务参数支持！',
            showWordLimit: true,
            maxlength: '200',
            props: {
              type: 'textarea'
            }
          },
          helper: {
            render (h) {
              return (< el-alert title="主要json格式" type="warning" />
              )
            }
          }
        }
      },

      {
        title: '备注',
        key: 'description',
        search: {
          disabled: true
        },
        show: false,
        width: 120,
        type: 'textarea',
        form: {
          disabled: false,
          component: {
            placeholder: '请输入备注',
            showWordLimit: true,
            maxlength: '200',
            props: {
              type: 'textarea'
            }
          }
        }
      }
    ]
  }
}
