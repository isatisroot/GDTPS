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
          <el-button class="button" icon="el-icon-success" @click="">保存</el-button>
        </div>
      </ul>
      <div class="container">
        <p class="title1" >佛山电器照明股份有限公司</p>
        <p class="title2">{{query.year+query.name}}表决票统计</p>
        <div class="search-gddmk">
<!--          element中使用原生@keyup.enter事件时需要加.native-->
          <el-autocomplete class="inline-input" v-model="searchValue0" :fetch-suggestions="querySearch0" placeholder="请输入股东姓名"
                           :trigger-on-focus="false" value-key="gdxm" @select="handleSelect" @keyup.enter.native="handleSelect"></el-autocomplete>
          <span style="margin: 10px">或</span>
          <el-autocomplete class="inline-input" v-model="searchValue" :fetch-suggestions="querySearch" placeholder="输入代码卡号"
                           :trigger-on-focus="false" value-key="gddmk" @select="handleSelect" @keyup.enter.native="handleSelect"></el-autocomplete>
<!--          <span>股东姓名或代码卡：</span><input v-model="searchValue" @keyup.enter="search()"></input><button @click="search">确认</button>-->
<!--           <el-button type="primary" @click="fn1">确认</el-button>-->
        </div>
        <br>
        <div>
          <table class="table2">
            <tr>
              <th rowspan="2">股东姓名</th>
              <th rowspan="2">股东代码</th>
              <th colspan="2">
                股票种类即持股数
              </th>
            </tr>
            <tr>
              <th>A股</th>
              <th>B股</th>
            </tr>

            <tr>
              <td>{{row.gdxm}}</td>
              <td>{{row.gddmk}}</td>
              <td>{{row.gzA}}</td>
              <td>{{row.gzB}}</td>
            </tr>
          </table>
          <el-divider></el-divider>
          <table class="table2">
            <tr >
              <th width="60">议案编号</th>
              <th>议案主题</th>
              <th>反对</th>
              <th>弃权</th>
              <th>是否回避</th>
              <th>回避表述</th>

            </tr>
            <tr v-for="(m,index) in motion" :key="index" >
              <td>{{index+1}}</td>
              <td>{{m}}</td>
              <td><el-checkbox v-model="fandui[index]"></el-checkbox></td>
              <td><el-checkbox v-model="qiquan[index]"></el-checkbox></td>
              <td><el-checkbox v-model="isHuibi[index]"></el-checkbox></td>
              <td><textarea v-model="huibi[index]"></textarea></td>

            </tr>
          </table>
<!--          <el-table :data="motion">-->
<!--            <el-table-column label="议案编号" type="index"></el-table-column>-->
<!--            <el-table-column label="议案主题" prop="name"></el-table-column>-->
<!--            <el-table-column label="反对">-->
<!--              <el-checkbox></el-checkbox>-->
<!--            </el-table-column>-->
<!--            <el-table-column label="弃权">-->
<!--              <el-checkbox></el-checkbox>-->
<!--            </el-table-column>-->
<!--          </el-table>-->
          <el-divider></el-divider>

<!--          <el-table :data="leijimotion">-->
<!--            <el-table-column label="议案编号" type="index"></el-table-column>-->
<!--            <el-table-column label="议案主题" prop="name"></el-table-column>-->
<!--            <el-table-column label="赞成">-->
<!--              <template slot-scope="scope">-->

<!--                <el-select v-model="scope.row.agree" required placeholder="请输入投赞成票数"  filterable allow-create-->
<!--                           default-first-option clearable>-->
<!--                  <el-option v-for="(val, id) in agreeList" :key="id" :value="val"></el-option>-->
<!--                </el-select>-->
<!--              </template>-->
<!--            </el-table-column>-->
<!--          </el-table>-->
          <h4>采用累计投票：</h4>
          <table class="table2">
            <tr >
              <th width="60">议案编号</th>
              <th>议案主题</th>
              <th>赞成</th>

            </tr>
            <tr v-for="(m,index) in leijimotion" :key="index" >
              <td>{{index+1}}</td>
              <td>{{m}}</td>
              <td>
                <el-select v-model="agree[index]" required placeholder="请输入投赞成票数"  filterable allow-create
                           default-first-option clearable>
                  <el-option v-for="(val, id) in agreeList" :key="id" :value="val"></el-option>
                </el-select>
              </td>

            </tr>
          </table>


        </div>
        <div style="text-align: center">
        <el-button type="primary" style="margin-top: 30px;" @click="next">下一张</el-button>

        </div>
        <el-divider></el-divider>
        <el-steps :active="active" finish-status="success" width="50%">
          <el-step v-for="(val, idx) in gdxmArray"><span slot="title"></span> </el-step>
        </el-steps>


      </div>

				
    </div>
	
</template>

<script>
import axios from 'axios'
export default {
  name: 'editor',
  data () {
    return {
      countRes: [],
      fandui: [],
      qiquan: [],
      isHuibi: [],
      huibi: [],
      countVoted: [],
      active: 0,
      agree: [],
      agreeList: [],
      countleijimotion: [],
      query: {
        year: '',
        name: ''
      },
      searchValue0: '',
      searchValue: '',
      motion: [],
      leijimotion: [],
      gdxmArray: [],
      gddmkArray: [],
      row: {}
    }
  },
  created () {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    axios.get(this.host + 'motion/' + this.query.year + '/' + this.query.name)
      .then(response => {
        this.gdxmArray = response.data['gdmsg']
        this.motion = response.data['motion']
        this.leijimotion = response.data['leijimotion']
        this.init()
      })
      .catch(error => {})
    // this.loadAll()
  },
  mounted () {

  },
  computed: {
    countlejimotion: function () {
      return {}
    }
  },
  methods: {
    init () {
      // this.countleijimotion = Array(this.leijimotion.length).fill({sum: 0})
      let n = this.leijimotion.length

      for (let i = 0; i < n; i++) {
        this.countleijimotion.push({name: this.leijimotion[i], sum: 0})
      }
    },
    next () {
      if (this.active++ > this.gdxmArray.lengthAdjust) this.active = 0
      this.countVoted.push(this.row.id)
      this.countRes.push({id: this.row.id, fanduiArray: this.fandui, qiquanArray: this.qiquan, isHuibi: this.isHuibi, descr: this.huibi})
      console.log(this.countRes)

      //统计累计投票赞成数


    },
    // 匹配输入框内容到表格中
    search () {
      for (let i = 0, len = this.gdxmArray.length; i < len; i++) {
        if (this.searchValue == this.gdxmArray[i].gdxm || this.searchValue == this.gdxmArray[i].gddmk) {
          this.row = this.gdxmArray[i]
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
    querySearch0 (queryString, cb) {
      var gdxmArray = this.gdxmArray
      var results = queryString ? gdxmArray.filter(this.createFilter0(queryString)) : gdxmArray
      // 调用 callback 返回建议列表的数据
      cb(results)
    },
    createFilter0 (queryString) {
      return (gdxmArray) => {
        console.log(gdxmArray)
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
          this.agreeList = []
          // 根据该股东持股数和议案数量计算有多少张选票
          for (let j = 0; j <= num; j++) {
            if (obj.gzA != 0) {
              this.agreeList.push(obj.gzA * j)
            }
            if (obj.gzB != 0) {
              this.agreeList.push(obj.gzB * j)
            }
          }
        }
      }
    }
  }
}
</script>
<style scoped>
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