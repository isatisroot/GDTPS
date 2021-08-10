<template>
	<div>
    <ul class="button-group">
      <div class="search-box" >
      <el-select v-model="query.year" placeholder="年份" class="handle-select mr10" filterable allow-create
                 clearable>
        <el-option v-for="(val, id) in yearList" :key="id" :value="val"></el-option>
      </el-select>

      <el-select v-model="query.name" label="会议类型" required placeholder="请选择会议类型">
        <el-option v-for="(val, id) in meetingName" :key="id" :value="val"></el-option>
      </el-select>

      <el-button type="warning" icon="el-icon-search" @click="handleSearch">搜索</el-button>
      <el-button type="warning" icon="el-icon-circle-plus" @click="dialogFormVisible=true" plain>新增会议</el-button>
        <el-button class="button" icon="el-icon-success" @click="submit">保存</el-button>

      </div>
<!--      <div class="button-group-left" style="margin-top: 10px">-->
<!--        <el-button class="button" icon="el-icon-circle-plus" @click="addMotion">新增议案</el-button>-->
<!--        <el-button class="button" icon="el-icon-success" @click="submit">保存</el-button>-->
<!--      </div>-->
    </ul>
    <el-dialog :visible.sync="dialogFormVisible"><span slot="title" style="margin-left: 300px;font-size: 30px;">新增会议</span>
      <AddMeeting></AddMeeting>
    </el-dialog>
    <div class="container">
    <div class="page">
      <div class="page-box">
        <el-form :model="form">
          <br>
          <el-divider style="margin-top: 10px">基本信息</el-divider>
          <el-form-item label="会议时间:">
            <el-col :span="10" style="padding-left: 0px">
              <el-form-item prop="date0">
                <el-date-picker placeholder="选择日期" v-model="form.date1" format="yyyy-MM-dd" value-format="yyyy-MM-dd"></el-date-picker>
              </el-form-item>
            </el-col>
            <!-- <el-col class="line" :span="2">-</el-col> -->
            <el-col :span="10">
              <el-form-item prop="date2">
                <el-time-picker placeholder="选择时间" v-model="form.date2" format="HH:mm" value-format="HH:mm"></el-time-picker>
              </el-form-item>
            </el-col>
          </el-form-item>
          <el-form-item prop="address" label="会议地点:" :label-width="formLabelWidth"><el-input v-model="form.address"></el-input></el-form-item>
          <el-divider style="margin-top: 10px">议案主题</el-divider>
          <div style="text-align: center;margin-top: -10px;margin-bottom: 15px">
            <span style="font-size: 10px;color:orangered">(✔表示采用累积投票)</span>
          </div>
          <el-form-item v-for="(m,idx) in motion">
              <li class="motion-li" style="list-style:none" >{{idx + 1}}.&nbsp;&nbsp;&nbsp;&nbsp;{{m.name }}
                <el-popconfirm title="确定删除这条议案吗？" @confirm="deleteMotion(idx, m.id)">
                  <i class="el-icon-delete"  style="position: absolute;right: 10px;top: 10px" slot="reference" ></i>
                </el-popconfirm>
              </li>
          </el-form-item>

<!--          <el-divider style="margin-top: 10px">累计投票议案</el-divider>-->
          <el-form-item v-for="(m,idx) in leijimotion" class="motion-li">
            <el-checkbox v-model="value" :disabled="value"></el-checkbox>
            <li style="list-style-type: none;display: inline-block;margin-left: 5px"  >{{m.name}}
                <el-popconfirm title="确定删除这条议案吗？" @confirm="deleteLeijiMotion(idx, m.id)">
                  <i class="el-icon-delete" style="position: absolute;right: 10px;top: 10px" slot="reference" ></i>
                </el-popconfirm>
              &nbsp;&nbsp;&nbsp;&nbsp;<li style="list-style:none" v-for="(submotion,idx) in m.submotions">{{idx+1}}.&nbsp;&nbsp;&nbsp;&nbsp;{{submotion.name}}</li>
            </li>
          </el-form-item>
          <el-form-item v-show="motionArray.length > 0">
            <div style="float: left; width: 90%" >
              <!-- <li v-for="(val, id) in motion.list" :key="id" style="list-style-type:none;">
                <el-input type="text" style="margin-bottom: 5px;" v-model="val.text"></el-input>
              </li> -->
              <!-- 使用作用域插槽，el-table是子组件，现在往子组件传<template>的内容，并获取里面的内容 " -->
              <el-table :data="motionArray" :show-header="false" ref="multipleTable" :row-class-name="tableRowClassName">
                <el-table-column align="center" width="58px" label="采用累积投票" prop="isleiji">
                <template slot-scope="scope">
                  <el-checkbox  v-model="scope.row.isleiji" @change="handleLeijiSelectionChange(scope)"></el-checkbox>
                </template>
                </el-table-column>
                <el-table-column prop=motion>
                  <template slot-scope="scope">
                    <el-input v-model="motionArray[scope.$index].motion"></el-input>
                    <div v-show="motionArray[scope.$index].isleiji">
                      <el-table :data="motionArray[scope.$index].leiji"  :show-header="false">
                        <el-table-column label="子编号"  align="center" type="index" :width="28"></el-table-column>
                        <el-table-column label="子议案主题" align="center" prop=leiji>
                          <template slot-scope="subscope">
                            <el-input v-model="motionArray[scope.$index].leijicontent[subscope.$index]"></el-input>
                          </template>
                        </el-table-column>
                      </el-table>
                      <div class="add-submotion" @click="addSubmotion(scope.$index)">
                        <i class="el-icon-circle-plus" style="margin-right:13px;color:white"></i>
                        <span style="color:white">新增子议案</span>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <!--                <el-table-column><button style="margin-left: 10px">上传附件</button></el-table-column>-->
                <!--            <el-table-column></el-table-column>-->


              </el-table>
              <!-- <el-input type="text" style="margin-bottom: 5px;"></el-input>
              <el-input type="text" style="margin-bottom: 5px;"></el-input> -->
            </div>
          </el-form-item>

          <div class="demo-block-control" @click="addMotion" v-if="motion != '' || leijimotion != ''">
<!--   <el-tooltip class="item" effect="dark" content="新增议案" placement="bottom">-->
<!--            <img src="../../assets/img/toggle_bg.png" width="500px" @click="addMotion" ></img>-->

            <div class="add-motion">
              <i class="el-icon-caret-bottom"></i>&nbsp;
              <span style="color: white" >新增议案</span>
            </div>

            <!--            </el-tooltip>-->
          </div>
          <div style="text-align: center" @click="addMotion" v-else >
<!--            <el-button type="success" icon="el-icon-circle-plus"  >新增议案</el-button>-->

            <button class="btn1">新增议案</button>
          </div>
<!--          <br>-->
          <el-divider style="margin-top: 10px">表决票说明</el-divider>
          <el-form-item prop="textarea"><el-input
              type="textarea"
              :rows="2"
              placeholder="请输入内容"
              v-model="form.descr">
          </el-input></el-form-item>

        </el-form>

      </div>
    </div>
    </div>
	</div>
</template>

<script>
import AnnualMeeting from '@/components/page/AnnualMeeting'
import AddMeeting from '@/components/page/AddMeeting'
import axios from '_axios@0.18.1@axios'
export default {
	  name: 'dashboard',
	  data () {
    var currenYear = new Date().getFullYear()
    return {

      value: true,
      formLabelWidth: '74px',
      form: {
        name: '',
        date1: '',
        date2: '',
        options: [],
        address: '',
        motion: '',
        desrc: ''
      },
      motionArray: [],
      addlejimotion: [],
      motion: [],
      leijimotion: [],
      meetingName: [],
      yearList: [currenYear - 1, currenYear + 1],
      address: '',
      query: {
        year: '',
        name: '',
        date: null
      },
      username: sessionStorage.username || localStorage.username,
      token: sessionStorage.token || localStorage.token,
      // res_data: {},
      ruleForm: {
        year: localStorage.year,
        meetingName: JSON.parse(localStorage.meetingName)
      },
      // tableData: [],
      dialogFormVisible: false,

      // yearList: [],
      // meetingNameList: [],
      name: localStorage.getItem('ms_username')

    }
  },
  components: {
    AnnualMeeting, AddMeeting
  },
  created () {
    this.query.year = JSON.parse(localStorage.getItem('year'))
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
    this.getData()
  },
  updated () {
    this.ruleForm.year = localStorage.getItem('year')
    this.ruleForm.meetingName = JSON.parse(localStorage.getItem('meetingName'))
  },
  computed: {
    role () {
      return this.name === 'admin' ? '超级管理员' : '普通用户'
    }
  },

  methods: {
    // 设置table每一行的颜色，当被勾选为累计议案是切换颜色
    tableRowClassName ({row, rowIndex}) {
      if (row.isleiji === true) {
        return 'warning-row'
      } else {
        return 'success-row'
      }
    },
    deleteBothMotionOrLeiji (id) {
      axios.delete(this.host + 'meeting/motion', {
        data: {id: id}}).then(response => {
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    deleteMotion (idx, id) {
      this.motion.splice(idx, 1)
      this.deleteBothMotionOrLeiji(id)
    },
    deleteLeijiMotion (idx, id) {
      this.leijimotion.splice(idx, 1)
      this.deleteBothMotionOrLeiji(id)
    },

    submit () {
      let url = this.host + 'update_meeting'
      axios.post(url, {
        year: this.query.year,
        name: this.query.name,
        form: this.form,
        motion: this.motion,
        leijimotion: this.leijimotion,
        addmotion: this.motionArray
      }).then(response => {
        // console.log(response.data)
        this.$message.success('数据更新成功！')
        location.reload()
      })
    },
    // download(){
    //   let self = this;
    //   let url = this.host + "download_file";
    //   let data = JSON.stringify({
    //     // user: self.$store.state.username,
    //     file_name: self.plist_file_name
    //   })
    //   console.log("data:", data)
    //   axios(
    //     {
    //       method: "post",
    //       url: url,
    //       data: data,
    //       responseType: "blob",    // 指定获取数据的类型为blob
    //     }
    // ).then(
    //     function (response) {
    //       data = response.data // 创建a标签并点击， 即触发下载
    //       let url = window.URL.createObjectURL(new Blob([data]))
    //       let link = document.createElement("a")
    //       link.style.display = "none"
    //       link.href = url
    //       link.setAttribute("download", self.plist_file_name)
    //       document.body.appendChild(link)
    //       link.click()
    //     }
    //   ).catch(function (err) {
    //     console.log(err)
    //   })
    //
    //
    // },
    uploadConfig (e, m) {
      console.log(m)
      let formData = new FormData()
      let data = JSON.stringify({
        user: 'username',
        name: m
      })
      formData.append('file', e.target.files[0])
      formData.append('data', data) // 上传文件的同时， 也可以上传其他数据
      let url = this.host + 'api/posts/upload'
      let config = {
        headers: {'Content-Type': 'multipart/form-data'}
      }
      axios.post(url, formData, config).then(function (response) {
        console.log(response.data)
      })
    },
    clickHiddenFile () {
      let oFile = document.getElementById('hiddenFile')
      oFile.click()
    },
    addMotion () {
      this.motionArray.push({'leijicontent': [], 'leiji': [{}, {}]})
    },

    // 新增子议案
    addSubmotion (index) {
      this.motionArray[index].leiji.push({})
    },
    // 当用户点击勾选框时，判断如果是勾选状态，则在motionArray数组中指定下标元素添加leiji属性，该指定下标元素（是一个对象）对应外层el-table某一行数据集合
    handleLeijiSelectionChange (scope) {
      if (scope.row.isleiji === true) {
        this.motionArray[scope.$index].leiji = [{}, {}]
      }
    },
    async handleSearch () {
      // 等待异步请求axios处理完成后再执行initSelectRow操作，因为后者需要等到tableData拿到数据后进行操作
      await this.getData()
      localStorage.setItem('year', JSON.stringify(this.query.year))
      localStorage.setItem('meetingName', JSON.stringify(this.query.name))
    },
    getData () {
      return axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name)
        .then(response => {
          // this.tableData = response.data['detail_list']
          // this.query.year = response.data['current']['year']
          this.form.date1 = response.data['current']['date']
          this.form.date2 = response.data['current']['date']
          // this.query.name = response.data['current']['name']
          // this.descr = response.data['current']['descr']
          this.motion = response.data['current']['motion']

          this.leijimotion = response.data['current']['leijimotion']
          this.form.address = response.data['current']['address']
          // console.log(res)
          // this.leijimotion = res
          this.meetingName = response.data['meeting_list']
          // this.share = response.data['sharehold']
          // this.gdxmArray = response.data['extr_shareholds']
        }).catch(error => {})
    },
    childByValue (childValue) {
      this.dialogFormVisible = childValue
    }
  }
}
</script>


<style scoped>
/deep/ .el-table .warning-row {
  /*background: oldlace;*/
  background: #b4e1e3;
}

/deep/.el-table .success-row {
  /*background: #f0f9eb;*/
  background: rgb(72 153 236 /10%);
}
.add-submotion {
  /*background: #67c23ac7;*/
  background: #53c8cd;
  border-radius: 5px;
  width: 80%;
  /*opacity: 0.7;*/
  text-align: center;
  margin: 0 auto;
  margin-top: 5px;
  cursor: pointer; /* 鼠标移入时变手指 */
}
.motion-li {
  /*鼠标悬浮时，由左往右动画填充颜色*/
  background: linear-gradient(to right, #FFCCBC 35%, ghostwhite 64%);
  background-size: 300% 100%;
  background-position:right bottom;
  transition: 1.5s ease-out;
}
.motion-li:hover {
  /*content: "";*/
  /*float: left;*/
  /*width: 10px;*/
  /*height: 10px;*/
  /*margin: 10px 0;*/
  /*background: linear-gradient(to right, #FF5722, #FFCCBC);*/
  /*opacity: 0.5;*/
  /*cursor:pointer;*/
  /*-webkit-transition:all .5s;*/
  /*transition:all .3s;*/
  /*border-radius: 10%;*/
  background-position: left bottom;
}

.btn1 {
  margin:10px 5px;
  padding:10px 60px;
  border-radius:10px;
  border:2px solid;
  font:16px 'Open Sans',sans-serif;
  text-transform:uppercase;
  background:none;
  outline:none;
  cursor:pointer;
  -webkit-transition:all .5s;
  transition:all .3s;

  color: #999;
  border-color: #f7c5a3;
  background:-webkit-linear-gradient(left,#a3f7bf,#a3f7bf) no-repeat;
  background:linear-gradient(to right, #f56405, #f56405) no-repeat;
  background-size:0% 100%;
}
.btn1:hover {
  background-size:100% 100%;
  color: #ffffff;
  text-shadow: 0 0 0.1em, 0 0 0.3em;
}
/*.fileinput-button {*/
/*  position: relative;*/
/*  display: inline-block;*/
/*  overflow: hidden;*/
/*}*/
/deep/ .el-table-column--selection .cell{
  padding-left: 0px;
}

.fileinput-button input{
  position:absolute;
  right: 0px;
  top:0px;
  opacity: 0;
  -ms-filter: 'alpha(opacity=0)';
  font-size: 200px;
}


	.search-box {
		font-family: "ms sans serif";
		font-size: 18px;
		font-weight: bolder;
	}

	.searchbox {
		margin-top: 20px;
		margin-bottom: 20px;
	}

	.el-row {
		margin-bottom: 20px;
	}

	.grid-content {
		display: flex;
		align-items: center;
		height: 100px;
	}

	.grid-cont-right {
		flex: 1;
		text-align: center;
		font-size: 14px;
		color: #999;
	}

	.grid-num {
		font-size: 30px;
		font-weight: bold;
	}

	.grid-con-icon {
		font-size: 50px;
		width: 100px;
		height: 100px;
		text-align: center;
		line-height: 100px;
		color: #fff;
	}

	.grid-con-1 .grid-con-icon {
		background: rgb(45, 140, 240);
	}

	.grid-con-1 .grid-num {
		color: rgb(45, 140, 240);
	}

	.grid-con-2 .grid-con-icon {
		background: rgb(100, 213, 114);
	}

	.grid-con-2 .grid-num {
		color: rgb(45, 140, 240);
	}

	.grid-con-3 .grid-con-icon {
		background: rgb(242, 94, 67);
	}

	.grid-con-3 .grid-num {
		color: rgb(242, 94, 67);
	}

	.user-info {
		display: flex;
		align-items: center;
		padding-bottom: 20px;
		border-bottom: 2px solid #ccc;
		margin-bottom: 20px;
	}

	.user-avator {
		width: 120px;
		height: 120px;
		border-radius: 50%;
	}

	.user-info-cont {
		padding-left: 50px;
		flex: 1;
		font-size: 14px;
		color: #999;
	}

	.user-info-cont div:first-child {
		font-size: 30px;
		color: #222;
	}

	.user-info-list {
		font-size: 14px;
		color: #999;
		line-height: 25px;
	}

	.user-info-list span {
		margin-left: 70px;
	}

	.mgb20 {
		margin-bottom: 20px;
	}

	.todo-item {
		font-size: 14px;
	}

	.todo-item-del {
		text-decoration: line-through;
		color: #999;
	}

	.schart {
		width: 100%;
		height: 300px;
	}

 i:hover {
  /*border-top-color: #287378;*/
  /*background: #ebf8e1;*/
  color: #ff0026;
}

.demo-block-control {
  padding-top: 3px;
  border: 1px solid #eaeefb;
  height: 24px;
  box-sizing: border-box;
  /*background: linear-gradient(to bottom, #FF5722, #FFCCBC);*/
  /*background: #409EFF;*/
  background: #5796d7;
  border-radius: 5px;
  width: 80%;
  /*opacity: 0.7;*/
  text-align: center;
  margin: 0 auto;
  /*background-color: #d3dce6;*/
  cursor: pointer;
  position: relative;
}
.add-motion{
  /*opacity: .5;*/
  transition: .5s;
  position: absolute;
  right: 34%;
}
.demo-block-control:hover .add-motion{
 /*opacity: 1;*/
  right: 42%;

}
.demo-block-control .add-motion i {
  color: #0cea2a;
  transition: .5s;
}
.demo-block-control:hover .add-motion i{
  color: white;
}
 .add-motion span {
   opacity: 0;
   line-height: 4px;
 }
.demo-block-control:hover .add-motion span{
  opacity: 1;
  font-size: 14px;
  /*text-shadow: 0 0 0.1em, 0 0 0.3em;*/
  /*color: #ffffff;*/
}


</style>
