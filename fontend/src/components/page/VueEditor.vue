<template xmlns="http://www.w3.org/1999/html">
    <div>
<!--        <div class="crumbs">-->
<!--        </div>-->
      <ul class="button-group">
        <div class="search-box">
<!--          <el-button  icon="" @click="" class="button" >合并统计</el-button>-->
          <!--                      <input type="file" value="" id="hiddenFile" @change="uploadConfig($event, m)" >-->
<!--        <span style="color:white">《《《 </span>-->
          <el-upload
              class="upload-demo"
              :action="this.host + 'upload'"
              :data="query"
              :on-change="handleChange"
              :file-list="fileList"
              accept=".xls"
          >
            <el-button size="small" type="warning" plain>导入网络投票结果</el-button>
            <!--            <div slot="tip" class="el-upload__tip">只能上传.xls文件,且不得重复上传同一份文件</div>-->
          </el-upload>
<!--          <el-button class="button" icon="el-icon-refresh" @click="refresh" v-if="isRecord">重新计票</el-button>-->
        </div>
      </ul>

      <div class="container">
        <p class="title1" >佛山电器照明股份有限公司</p>
        <p class="title2">{{query.name}}表决票统计</p>
        <div class="search-gddmk">
          <!-- el-autocomplete标签是在vue之上的封装，所以在element中要使用原生回车键监听事件（@keyup.enter事件）时需要加.native
          该事件是敲击回车后调用handleSelect方法-->
          <!--@select是鼠标选中某个建议后调用handleSelect方法-->
          <el-autocomplete class="inline-input" v-model="searchValue" :fetch-suggestions="querySearchGddmk" placeholder="请扫描股东代码号"
                            value-key="gddmk" @select="handleSelect" @keyup.enter.native="handleSelect">
          </el-autocomplete>
          <span style="margin: 10px">或</span>
          <!--trigger-on-focus是el-autocomplete标签封装的属性，表示是否在输入框 focus时显示建议列表-->
          <el-autocomplete class="inline-input" v-model="searchValue0" :fetch-suggestions="querySearchGdxm" placeholder="输入股东姓名"
                           :trigger-on-focus="false" value-key="gdxm" @select="handleSelect" @keyup.enter.native="handleSelect">
          </el-autocomplete>
        </div>
        <el-divider></el-divider>
        <div class="page">
        <div class="page-box">
        <el-form :model="form" ref="voteForm">

          <br>
          <el-divider style="margin-top: 10px">基本信息</el-divider>
          <el-form-item label="股东姓名：">{{row.gdxm}}</el-form-item>
          <el-form-item label="股东代码卡：">{{row.gddmk}}</el-form-item>
          <el-form-item label="A股：" v-if="row.gzA > 0" >{{row.gzA}}</el-form-item>
          <el-form-item label="B股：" v-else-if="row.gzB > 0">{{row.gzB}}</el-form-item>
          <el-form-item label="持股数：" v-else></el-form-item>
          <el-divider>议案主题</el-divider>
          <template>
            <el-form-item v-for="(m, index) in motion">
              <template>
                <li>{{ m.name }}</li>
                <el-radio-group v-model="m.checked" :disabled="!row.id" >
                  <el-radio :label="1" >赞成</el-radio>
                  <el-radio :label="2" >反对</el-radio>
                  <el-radio :label="3" >弃权</el-radio>
                </el-radio-group>
                <div style="position: relative;float: right; display: inline-block">
                  <span style="margin-left: 15px">是否回避：</span><el-switch v-model="m.ishuibi"></el-switch>
                  <span style="margin-left: 15px;margin-right: 10px">回避表述：</span><el-input v-model="m.descr" :disabled="!m.ishuibi" style="display: inline-block;width: 200px"></el-input>
                </div>
              </template>

            </el-form-item>
          </template>
          <br>
          <template>
            <el-form-item v-for="(m, index) in leijimotion" >
              <template>
                <p style="text-align:center;">{{m.name}}</p>
                <li v-for="submotion in m.submotions">{{submotion.name}}&nbsp;&nbsp;
                <!--              <el-select v-model="agree[index]"  required placeholder="请输入投赞成票数"  filterable allow-create default-first-option-->
                <!--                          clearable @blur="selectBlur($event, index)" @keyup.enter.native="enterFn">-->
                <!--                <el-option v-for="(val, id) in agreeList" :key="id" :value="val"></el-option>-->
                <!--              </el-select>-->
                <el-autocomplete
                    class="inline-input autocom-sty"
                    v-model="submotion.agree"
                    :fetch-suggestions="querySearch3"
                    placeholder="请输入赞成票数"
                    :disabled="!row.id"
                    @change="validate(submotion)"
                ></el-autocomplete>
                <el-alert
                    :title="tip"
                    type="error"
                    show-icon
                    v-if="errorTip[index]">
                </el-alert>
                </li>
                <br>
              </template>
            </el-form-item>
          </template>
          <el-alert
              title="输入的投票总数数不得大于可投票总数"
              type="error"
              @close="showAlert=false"
          v-show="showAlert">
          </el-alert>
          <el-divider></el-divider>
        </el-form>
        </div>
        </div>
        <div style="text-align: center">
          <el-button class="button" style="margin: 20px;" icon="el-icon-finished" @click="submit" v-if="showDone">提交</el-button>

<!--          <button class=""  @click="finish" v-if="showDone">完成</button>-->
        <el-button type="primary" style="margin: 20px;" @click="next" v-else>下一张</el-button>

        </div>
<!--        <div style="text-align: center">-->
<!--        <el-steps :active="active" finish-status="success" :space="40" simple>-->
<!--          <el-step align-center  v-for="(val, idx) in step"  icon="el-icon-s-custom"><span slot="title">{{idx + 1}}</span> </el-step>-->
<!--        </el-steps>-->
<!--      </div>-->
      </div>
    </div>
	
</template>

<script>
import axios from 'axios'

export default {
  name: 'editor',
  data () {
    return {
      validNum: false,
      fileList: [],
      validate_num: true,
      showAlert: false,
      test: 1,
      tip: '',
      errorTip: [],
      isRecord: false,
      showDone: false,
      form: {
        checked: [],
        isHuibi: [],
        desc: []
      },
      countVoted: [],
      active: 0,
      agree: [],
      agreeList: [],
      query: {
        year: '',
        name: ''
      },
      searchValue0: '',
      searchValue: '',
      motion: [],
      leijimotion: [],
      gdMsgArray: [],
      voteArray: [],
      row: {},
      step: [],
      nextStep: 0
    }
  },
  created () {
    this.query.year = JSON.parse(localStorage.getItem('year'))
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    axios.get(this.host + 'motion/' + this.query.year + '/' + this.query.name)
      .then(response => {
        // console.log(response.data)
        this.gdMsgArray = response.data['gdmsg']
        // this.step = new Array(this.gdMsgArray.length).fill()
        let res1 = response.data['motion']
        this.leijimotion = response.data['leijimotion']
        res1.forEach(item => {
          item.checked = 0
          item.ishuibi = false
          item.descr = ''
        })
        // res2.forEach(item => {
        //   item.agree = null
        // })
        this.motion = res1

        // this.form.checked = new Array(this.motion.length).fill(1)
        // this.form.isHuibi = new Array(this.motion.length).fill(false)
        // this.form.desc = new Array(this.motion.length).fill(null)
        // console.log(this.gdMsgArray)
        // this.init()
      })
      .catch(error => {
        console.log(error)
      })
    // this.loadAll()
  },
  mounted () {

  },
  watch: {
    // 深度监听，监听数组中的对象
    'leijimotion': {
      handler: function (newval) {
        // console.log(newval)
        // newval是数组leijimotion里的一个个对象
        newval.forEach(item => {
          let num = 0
          let _sum = 0
          var regPos = /^[0-9]*$/
          // 先判断该累计议案下有多少个子议案
          let submotionNum = item.submotions.length
          // 该累计议案总计有多少赞成票
          let totalVote = 0
          if (this.row.gzA) {
            totalVote = this.row.gzA * submotionNum
          } else {
            totalVote = this.row.gzB * submotionNum
          }
          // 剩余票数
          let remainingVote = totalVote
          // 遍历该累计议案下的子议案
          item.submotions.forEach(subItem => {
            // 获取该子议案投票数
            let subItemVote = subItem.agree
            remainingVote -= subItemVote
            if (remainingVote < 0) {
              // this.$message.error('该累计议案总赞成数不得大于' + totalVote)
              this.$notify({
                title: '警告！',
                type: 'warning',
                message: '该累计议案总赞成数不得大于' + totalVote,
                duration: 0
              })
            }
            if (subItemVote) {
              console.log(regPos.test(subItemVote))
              if (!regPos.test(subItemVote)) {
                this.$message.error('请输入纯数字!')
              }
            }
            // 根据用户已经输入的赞成票，计算剩余可投赞成列表中，该列表的数据可在下面方法中提供输入建议
            // if (subItem.agree) {
            //   num += 1
            //   _sum += parseInt(subItem.agree)
            // }
            // let rest1 = totalVote - _sum
            // let rest2 = submotionNum - num
            // this.agreeList = []

            // for (let j = 0; j <= rest2; j++) {
            //   let gza = this.row.gzA
            //
            //   let gzb = this.row.gzB
            //   if (gza !== 0 & gza * j <= rest1) {
            //     this.agreeList.push({value: gza * j + ''})
            //   }
            //   if (gzb !== 0 & gzb * j <= rest1) {
            //     this.agreeList.push({value: gzb * j + ''})
            //   }
            // }
          })
        })
      },
      deep: true
    }
  },
  // beforeUpdate () {
  //   console.log('beforeUpdate', this.motion)
  // },
  // updated () {
  //   console.log('updated', this.motion)
  // },
  computed: {
    count1 () {
      return function (checked, m) {
        return m.sumZanA
      }
    }
  },
  methods: {
    handleChange (file, fileList) {
      // this.fileList = fileList.slice(-3);
    },
    refresh () {
      axios.get(this.host + 'refresh/', {params: {year: this.query.year, name: this.query.name}})
    },
    validate (submotion) {
      // 判断是否是数字
      var regPos = /^[0-9]*$/
      let num = submotion.agree
      if (num) {
        if (!regPos.test(num)) {
          this.$message.error('请输入纯数字!')
          this.validNum = false
          return false
        }
        this.validNum = true
        return true
      } else {
        this.validNum = false
        return false
      }
    },

    selectBlur (e, index) {
    },
    init () {
      // this.countleijimotion = Array(this.leijimotion.length).fill({sum: 0})
      let n = this.leijimotion.length

      for (let i = 0; i < n; i++) {
        this.countleijimotion.push({name: this.leijimotion[i], sum: 0})
      }
    },
    submit () {
      // console.log(this.countVoted)
    },
    next () {
      // 校验投票总数是否大于可投票总数
      this.row.leijimotion.forEach(item => {
        let leijimotionNum = item.submotions.length
        let total = 0
        if (this.row.gzA) {
          total = this.row.gzA * leijimotionNum
        } else {
          total = this.row.gzB * leijimotionNum
        }
        let _sum = 0
        item.submotions.forEach(subItem => {
          if (subItem.agree) {
            _sum += parseInt(subItem.agree)
          }
          if (_sum > total) {
            this.showAlert = true
            return null
          }
        })
      })

      if (this.validate_num == false) {
        this.$alert('请输入纯数字', '错误提示', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: 'info',
              message: `action: ${action}`
            })
          }
        })
      } else {
        this.row.motion = this.motion
        this.row.leijimotion = this.leijimotion
        axios.post(this.host + 'teller', {
          row: this.row
        }).then(response => {
          this.$message({
            type: 'success',
            message: `数据提交成功`
          })
          // 当数据提交成功后将用户输入的数据清空，以便用户输入下一个股东投票数据
          this.searchValue = ''
          this.searchValue0 = ''
          this.row = {}
          this.motion.forEach(item => {
            item.checked = 0
            item.ishuibi = false
            item.desc = ''
          })
          this.leijimotion.forEach(item => {
            item.submotions.forEach(subItem => {
              subItem.agree = null
            })
          })
        }).catch(error => { console.log(error) })
      }
    },
    // 匹配输入框内容到表格中
    search () {
      for (let i = 0, len = this.gdMsgArray.length; i < len; i++) {
        if (this.searchValue == this.gdMsgArray[i].gdxm || this.searchValue == this.gdMsgArray[i].gddmk) {
          this.row = this.gdMsgArray[i]
          // console.log(this.row)
        }
      }
    },
    // 向服务端缓存将与输入相关的内容
    loadAll () {
      var gdid = []
      axios.post(this.host + 'loadall', {
        gdid: gdid
      }).then(response => {
        this.gdMsgArray = response.data
      }).catch(error => {})
    },

    querySearch3 (queryString, cb) {
      var agreeList = this.agreeList
      var results = queryString ? agreeList.filter(this.createFilter3(queryString)) : agreeList
      cb(results)
    },
    createFilter3 (queryString) {
      return (agreeList) => {
        return (agreeList.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },

    querySearchGdxm (queryString, cb) {
      var gdMsgArray = this.gdMsgArray
      var results = queryString ? gdMsgArray.filter(this.createFilterGdxm(queryString)) : gdMsgArray
      // 调用 callback 返回建议列表的数据
      cb(results)
    },
    createFilterGdxm (queryString) {
      return (gdObj) => {
        // console.log(gdMsgArray)
        return (gdObj.gdxm.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },

    // 输入建议，queryString用户输入字符，当用户输入股东代码卡字符后提供输入建议，例如用户只输入了08两个字符，然后就提供08开头的数据， cb回调函数返回建议内容
    querySearchGddmk (queryString, cb) {
      var gdMsgArray = this.gdMsgArray
      // 二元表达式，当没有输入字符串时返回整个gdMsgArray数组到el-autocomplete模板中
      var results = queryString ? gdMsgArray.filter(this.createFilterGddmk(queryString)) : gdMsgArray
      // 调用 callback 返回建议列表的数据
      cb(results)
    },

    createFilterGddmk (queryString) {
      // 闭包的方式才能将queryString参数传入进来，gdObj是gdMsgArray调用filter方法后逐一传入进来的数组里的元素
      return (gdObj) => {
        // 如果该字符出席在gddmk的值里，判断为真则返回整个gdObj
        return (gdObj.gddmk.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    handleSelect (item) {
      let num = this.leijimotion.length
      let obj = {}
      for (let i = 0, len = this.gdMsgArray.length; i < len; i++) {
        obj = this.gdMsgArray[i]

        if (item.gdxm == obj.gdxm || item.gddmk == obj.gddmk || this.searchValue0 == obj.gdxm || this.searchValue == obj.gddmk) {
          this.row = this.gdMsgArray[i]
          console.log(this.row)
          this.agreeList = []
          // 根据该股东持股数和议案数量计算有多少张选票
          for (let j = 0; j <= num; j++) {
            if (obj.gzA != 0) {
              // console.log( this.leijimotion[j].name)
              this.agreeList.push({value: obj.gzA * j + ''})
            }
            if (obj.gzB != 0) {
              this.agreeList.push({value: obj.gzB * j + ''})
            }
          }
          this.gdMsgArray.splice(i, 1)
        }
      }
      // console.log(this.agreeList)
    }
  }
}
</script>
<style scoped>
.autocom-sty {
  float: right;
}
li {
  list-style: none;
  margin-bottom: 10px;
  margin-top: 10px;
}
.tongji-btn {
  /*float:right;*/
}
/deep/ .upload-demo{
  display: inline-block;
  margin-bottom: 10px;
}
/deep/ .el-upload--text{
  width: 0;
  height: 0;
}
.bar1 {
  background: #ef6e45;
  /*background: linear-gradient(0.25turn, #03A9F4, #ebf8e1, #B2DFDB);*/
  padding: 9px 15px;
  border-radius: 3px;
  color: #455A64;
  /*color: red;*/
  font-size: 12px;
  font-weight: bolder;
  font-family: "YouYuan";
  opacity: 0.8;

}
 /deep/ .el-step__icon  {
  height: 15px;
  width: 15px;
}
    .editor-btn{
        margin-top: 20px;
    }
    .search-gddmk {
      text-align: center;
      font-size: 15px;
    }
    .search-gddmk input{
      height: 20px;
      margin-right: 5px;
    }
    .table-chapiao {
      width:50%;
      margin: auto;
      text-align: center;
      border-collapse: collapse;
    }


</style>
