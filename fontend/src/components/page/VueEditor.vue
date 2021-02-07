<template xmlns="http://www.w3.org/1999/html">
    <div>
        <div class="crumbs">
<!--            <el-breadcrumb separator="/">-->
<!--                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>-->
<!--                <el-breadcrumb-item>编辑器</el-breadcrumb-item>-->
<!--            </el-breadcrumb>-->
        </div>
      <ul class="button-group">
        <div class="button-group-left">
          <!--        <el-button class="button" icon="el-icon-circle-plus" @click="addRow">增加</el-button>-->
          <!--        <el-button class="button" icon="el-icon-delete" @click="handleDelete(row.index,row)" >删除</el-button>-->
<!--          <el-button class="button" icon="el-icon-printer" @click="">统计表</el-button>-->
<!--          <el-button class="button" icon="el-icon-printer" @click="" v-print="">表决结果</el-button>-->
<!--          <el-button class="button" icon="el-icon-success" @click="submit">保存</el-button>-->
        </div>
      </ul>
      <div class="container" v-if="isRecord">
        <div style="text-align: center">
          <h2 class="title1">表决票已统计！</h2>
        <img src="~@/assets/img/voted.png" height="400" width="400" >

        </div>
      </div>
      <div class="container" v-else>
        <p class="title1" >佛山电器照明股份有限公司</p>
        <p class="title2">{{query.year+query.name}}表决票统计</p>
        <div class="search-gddmk">
<!--          element中使用原生@keyup.enter事件时需要加.native-->
          <el-autocomplete class="inline-input" v-model="searchValue0" :fetch-suggestions="querySearch0" placeholder="请输入股东姓名"
                           :trigger-on-focus="false" value-key="gdxm" @select="handleSelect" @keyup.enter.native="handleSelect"></el-autocomplete>
          <span style="margin: 10px">或</span>
          <el-autocomplete class="inline-input" v-model="searchValue" :fetch-suggestions="querySearch" placeholder="输入代码卡号"
                           value-key="gddmk" @select="handleSelect" @keyup.enter.native="handleSelect"></el-autocomplete>
<!--          <span>股东姓名或代码卡：</span><input v-model="searchValue" @keyup.enter="search()"></input><button @click="search">确认</button>-->
<!--           <el-button type="primary" @click="fn1">确认</el-button>-->
        </div>
        <el-divider></el-divider>
        <div class="page">
        <div class="page-box">
        <el-form :model="form" >
<!--          <div>e</div>-->
<!--          <p></p>-->
          <br>
          <el-divider style="margin-top: 10px">基本信息</el-divider>
          <el-form-item label="股东姓名：">{{row.gdxm}}</el-form-item>
          <el-form-item label="股东代码卡：">{{row.gddmk}}</el-form-item>
          <el-form-item label="A股：" v-if="row.gzA > 0" >{{row.gzA}}</el-form-item>
          <el-form-item label="B股：" v-else-if="row.gzB > 0">{{row.gzB}}</el-form-item>
          <el-form-item label="持股数：" v-else></el-form-item>
          <el-divider>议案主题</el-divider>

          <el-form-item v-for="(m, index) in motion">
            <template>
              <li>{{ m.name }}</li>
              <el-radio-group v-model="m.checked" :disabled="form.isHuibi[index]">
                <el-radio :label="1" >赞成</el-radio>
                <el-radio :label="2">反对</el-radio>
                <el-radio :label="3">弃权</el-radio>
              </el-radio-group>
              <div style="position: relative;float: right; display: inline-block">
              <span style="margin-left: 15px">是否回避：</span><el-switch v-model="form.isHuibi[index]"></el-switch>
              <span style="margin-left: 15px;margin-right: 10px">回避表述：</span><el-input v-model="form.desc[index]" :disabled="!form.isHuibi[index]" style="display: inline-block;width: 200px"></el-input>
              </div>
            </template>

          </el-form-item>
          <br>
          <el-divider v-if="leijimotion">累计投票议案</el-divider>
          <el-form-item v-for="(m, index) in leijimotion">
            <template>
<!--              <br>-->
              <li >{{m.name}}</li>
<!--              <el-select v-model="agree[index]"  required placeholder="请输入投赞成票数"  filterable allow-create default-first-option-->
<!--                          clearable @blur="selectBlur($event, index)" @keyup.enter.native="enterFn">-->
<!--                <el-option v-for="(val, id) in agreeList" :key="id" :value="val"></el-option>-->
<!--              </el-select>-->
              <el-autocomplete
                  class="inline-input"
                  v-model="agree[index]"
                  :fetch-suggestions="querySearch3"
                  placeholder="请输入赞成票数"
                  @select="handleSelect"
                  @blur="validate(index)"
              ></el-autocomplete>
              <el-alert
                  :title="tip"
                  type="error"
                  show-icon
                  v-if="errorTip[index]">
              </el-alert>
            </template>
          </el-form-item>
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
        <el-steps :active="active" finish-status="success" :space="40" simple>
          <el-step align-center  v-for="(val, idx) in step"  icon="el-icon-s-custom"><span slot="title">{{idx + 1}}</span> </el-step>
        </el-steps>
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
      gdxmArray: [],
      // gddmkArray: [],
      row: {},
      step: [],
      nextStep: 0
    }
  },
  created () {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    axios.get(this.host + 'motion/' + this.query.year + '/' + this.query.name)
      .then(response => {
        this.gdxmArray = response.data['gdmsg']
        // this.motion = response.data['motion']
        this.leijimotion = response.data['leijimotion']
        let res = response.data['motion']
        res.forEach(item => {
          item.checked = []
        })
        this.motion = res
        this.step = new Array(this.gdxmArray.length).fill()
        // this.form.checked = new Array(this.motion.length).fill(1)
        this.form.isHuibi = new Array(this.motion.length).fill(false)
        // this.form.desc = new Array(this.motion.length).fill(null)
        // console.log(this.gdxmArray)
        this.init()
      })
      .catch(error => {})
    // this.loadAll()
  },
  mounted () {

  },
  computed: {
    count: function () {
      this.countVoted.push({id: this.row.id, motion1: this.form, motion2: this.agree})
      return this.countVoted
    }
  },
  methods: {
    validate (index) {
      console.log(this.agree[index])
      // if (typeof (this.agree[index]) === 'undefined') {
      //   this.errorTip[index] = true
      //   this.tip = '不能为空'
      //   this.$forceUpdate() // 强制更新
      // } else {
      //   this.errorTip[index] = false
      //   this.$forceUpdate()
      // }
      if (this.agree[index] > this.row.gzA && this.agree[index] > this.row.gzB) {
        this.errorTip[index] = true
        this.tip = '输入的值大于当前股东可投票数'
        this.$forceUpdate()
        console.log(this.errorTip)
        // this.$message({
        //   type: 'warning',
        //   message: `输入的值大于当前股东可投票数`
        // })
      }
    },
    enterFn (e) {
      console.log(e)
      // let dom = document.getElementsByClassName("tbody-input")
      // let dom = e.target
      // let nextInput = dom.nextSibling
      // nextInput.focus()
      // console.log(nextInput)
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
      console.log(this.countVoted)
    },
    next () {
      this.motion.forEach(item => {
        console.log(item.checked)
      })
      if (this.agree.length < this.leijimotion.length) {
        this.$message({
          type: 'error',
          message: `赞成票不能为空`
        })
      }else if (this.form.checked.length < this.motion.length) {
        this.$message({
          type: 'error',
          message: `议案表决票不能为空`
        })
      }else{
        if (this.active++ == this.step.length - 1) {
          // this.showDone = true
          // this.active = 0
          this.$alert('是否提交数据', '表决统计', {
            confirmButtonText: '确定',
            callback: action => {
              axios.post(this.host + 'record', {
                countVoted: this.countVoted,
                motion: this.motion,
                leijimotion: this.leijimotion
              }).then(response => {
                this.$message({
                  type: 'success',
                  message: `数据提交成功`
                })
                // this.isRecord = true
                this.$router.push('/tabs')
              }).catch(error => { console.log(error) })
            }
          })
        }
        console.log(this.form)
        let motion1 = this.form
        this.countVoted.push({id: this.row.id, motion1: motion1, motion2: this.agree})
        // this.count()
        console.log(this.countVoted)
        this.searchValue = ''
        this.searchValue0 = ''
        this.row = {}
        // this.form.checked = new Array(this.motion.length).fill(1)
        // this.form.isHuibi = new Array(this.motion.length).fill(false)
        // this.form.desc = new Array(this.motion.length).fill(null)
        this.form = {
          checked: [],
          isHuibi: [],
          desc: ''
        }
        this.agree = []
      }

    },
    // 匹配输入框内容到表格中
    search () {
      for (let i = 0, len = this.gdxmArray.length; i < len; i++) {
        if (this.searchValue == this.gdxmArray[i].gdxm || this.searchValue == this.gdxmArray[i].gddmk) {
          this.row = this.gdxmArray[i]
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
        this.gdxmArray = response.data
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

    querySearch0 (queryString, cb) {
      var gdxmArray = this.gdxmArray
      var results = queryString ? gdxmArray.filter(this.createFilter0(queryString)) : gdxmArray
      // 调用 callback 返回建议列表的数据
      cb(results)
    },
    createFilter0 (queryString) {
      return (gdxmArray) => {
        // console.log(gdxmArray)
        return (gdxmArray.gdxm.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },

    // 输入建议，queryString用户输入字符， cb回调函数返回建议内容
    querySearch (queryString, cb) {
      var gdxmArray = this.gdxmArray
      var results = queryString ? gdxmArray.filter(this.createFilter(queryString)) : gdxmArray
      // 调用 callback 返回建议列表的数据
      cb(results)
    },

    createFilter (queryString) {
      return (gdxmArray) => {
        return (gdxmArray.gddmk.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    handleSelect (item) {
      let num = this.leijimotion.length
      let obj = {}
      for (let i = 0, len = this.gdxmArray.length; i < len; i++) {
        obj = this.gdxmArray[i]

        if (item.gdxm == obj.gdxm || item.gddmk == obj.gddmk || this.searchValue0 == obj.gdxm || this.searchValue == obj.gddmk) {
          this.row = this.gdxmArray[i]
          // console.log(this.row)
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
          this.gdxmArray.splice(i, 1)
        }
      }
      // console.log(this.agreeList)
    }
  }
}
</script>
<style scoped>
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




 .page,.page-box{
   margin: 0 auto;
   width: 650px;
   padding: 50px 0 0 60px;
   background: #fff;
   /*background: url("../../assets/img/box-bg.jpg");*/
   border-radius: 20px;
   text-align: justify;
 }
 .page-box{
   padding: 0 60px 40px 0;
 }
 .page{
   position: relative;
   /*margin-left: 0;*/

   filter: drop-shadow(0px 0px 15px #bbb);
 }
 .page:before{
   content: '';
   display: block;
   position: absolute;
   right:-60px;
   top:0;
   width: 60px;
   height: 50px;
   background: linear-gradient(42deg, #ddd 30%, rgba(0,0,0,0) 40%);
 }
</style>