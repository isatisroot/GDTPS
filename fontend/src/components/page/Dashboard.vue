<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="8">

				<!-- 查询与新增年度会议功能卡 -->
				<el-card shadow="hover" style="height:252px;text-align: center;">
					<div slot="header" class="clearfix">
						<span class="search-box">选择股东大会年度</span>
					</div>
          <AnnualMeeting v-on:childByValue="childByValue"></AnnualMeeting>
				</el-card>
				<!-- 点击新增button之后弹出具有填写表单功能的弹窗 -->
				<el-dialog :visible.sync="dialogFormVisible"><span slot="title" style="margin-left: 300px;font-size: 30px;">新增会议</span>
<!--					<el-form :model="form" :rules="rules" ref="form">-->
<!--						<el-form-item label="会议名称" prop="name" :label-width="formLabelWidth">-->
<!--							<el-input v-model="form.name" autocomplete="off"></el-input>-->
<!--						</el-form-item>-->

<!--						<el-form-item label="会议时间" :label-width="formLabelWidth" required>-->
<!--							<el-col :span="10" style="padding-left: 0px">-->
<!--								<el-form-item prop="date0">-->
<!--									<el-date-picker placeholder="选择日期" v-model="form.date1" format="yyyy-MM-dd" value-format="yyyy-MM-dd"></el-date-picker>-->
<!--								</el-form-item>-->
<!--							</el-col>-->
<!--							&lt;!&ndash; <el-col class="line" :span="2">-</el-col> &ndash;&gt;-->
<!--							<el-col :span="10">-->
<!--								<el-form-item prop="date2">-->
<!--									<el-time-picker placeholder="选择时间" v-model="form.date2" format="HH:mm" value-format="HH:mm"></el-time-picker>-->
<!--								</el-form-item>-->
<!--							</el-col>-->
<!--						</el-form-item>-->
<!--						<el-form-item prop="address" label="会议地点" :label-width="formLabelWidth" default-first-option>-->
<!--							&lt;!&ndash; <el-cascader :options="options" v-model="form.address"></el-cascader> &ndash;&gt;-->
<!--							<el-input v-model="form.address"></el-input>-->
<!--						</el-form-item>-->
<!--						<el-form-item label="会议议案" :label-width="formLabelWidth">-->
<!--							&lt;!&ndash; <template slot-scope="scope"> &ndash;&gt;-->
<!--							<div style="float: left; width: 90%">-->
<!--								&lt;!&ndash; <li v-for="(val, id) in motion.list" :key="id" style="list-style-type:none;">-->
<!--									<el-input type="text" style="margin-bottom: 5px;" v-model="val.text"></el-input>-->
<!--								</li> &ndash;&gt;-->
<!--								&lt;!&ndash; 使用作用域插槽，el-table是子组件，现在往子组件传<template>的内容，并获取里面的内容 &ndash;&gt;-->
<!--								<el-table :data="motionArray" :show-header="false">-->
<!--									<el-table-column prop=motion>-->
<!--										<template slot-scope="scope">-->
<!--											<el-input v-model="motionArray[scope.$index].motion"></el-input>-->
<!--										</template>-->
<!--									</el-table-column>-->
<!--								</el-table>-->
<!--								&lt;!&ndash; <el-input type="text" style="margin-bottom: 5px;"></el-input>-->
<!--								<el-input type="text" style="margin-bottom: 5px;"></el-input> &ndash;&gt;-->
<!--							</div>-->
<!--							<div style="float:right">-->
<!--								<el-button icon="el-icon-circle-plus" type="success" @click="addMotion"></el-button>-->
<!--							</div>-->
<!--							&lt;!&ndash; </template> &ndash;&gt;-->
<!--						</el-form-item>-->
<!--					</el-form>-->
<!--					<div class="edit_dev">-->
<!--						<el-transfer v-model="value" :data="gddata" :titles="['可添加股东信息列表', '已添加股东信息列表']"></el-transfer>-->
<!--					</div>-->

<!--					<div slot="footer" class="dialog-footer">-->
<!--						<el-button @click="dialogFormVisible = false">取 消</el-button>-->
<!--						<el-button type="primary" @click="submitAdd('form')">确 定</el-button>-->
<!--						&lt;!&ndash; <el-button type="primary">-->
<!--							<router-link :to="'/table'"><span style="color: white;">确定</span></router-link>-->
<!--						</el-button> &ndash;&gt;-->
<!--					</div>-->
          <AddMeeting></AddMeeting>
				</el-dialog>
			</el-col>
			<el-col :span="16">
				<!-- 会议文件展示功能卡 -->
				<el-card shadow="hover" style="height:403px;">
					<div slot="header" class="clearfix">
						<span>会议议案</span>
						<el-button style="float: right; padding: 3px 0" type="text">添加</el-button>
					</div>
					<el-table :show-header="false" :data="todoList" style="width:100%;">
						<el-table-column width="40">
							<template slot-scope="scope">
								<el-checkbox v-model="scope.row.status"></el-checkbox>
							</template>
						</el-table-column>
						<el-table-column>
							<template slot-scope="scope">
								<div class="todo-item" :class="{'todo-item-del': scope.row.status}">{{scope.row.title}}</div>
							</template>
						</el-table-column>
						<el-table-column width="60">
							<template>
								<i class="el-icon-edit"></i>
								<i class="el-icon-delete"></i>
							</template>
						</el-table-column>
					</el-table>
				</el-card>
			</el-col>
		</el-row>
    
	</div>
</template>

<script>
	import {
	  EventBus
	} from '../../api/event_bus.js'
import axios from 'axios'
  import AnnualMeeting from "@/components/page/AnnualMeeting";
	import AddMeeting from "@/components/page/AddMeeting";
export default {
	  name: 'dashboard',
	  data () {
    return {
	      username: sessionStorage.username || localStorage.username,
	      token: sessionStorage.token || localStorage.token,
	      res_data: {},
	      ruleForm: {
	        year: null
	      },
	      tableData: [],
	      // gddata: [],
	      // value: [],
	      // dialogTableVisible: false,
	      dialogFormVisible: false,
	      // form: {
	      //   name: '',
	      //   date1: '',
	      //   date2: '',
	      //   options: [],
	      //   address: '',
	      //   motion: ''
	      // },

	      // motionArray: [{}],
	      // formLabelWidth: '120px',
	      // date: null,
	      meetingName: '',
	      yearList: [],
	      meetingNameList: [],
	      name: localStorage.getItem('ms_username'),
	      todoList: [{
	        title: '关于与广东省广晟财务有限公司签署《金融服务协议》的议案',
	        status: false
	      },
	      {
	        title: '关于修订《公司章程》的议案',
	        status: false
	      },
	      {
	        title: '关于续聘2020年度审计机构的议案',
	        status: false
	      },
	      {
	        title: '关于XXXXXX的议案',
	        status: false
	      },
	      {
	        title: '关于XXXXXX的议案',
	        status: false
	      }

	      ]
	    }
  },
  components: {
    AnnualMeeting, AddMeeting
  },

	  computed: {
	    role () {
	      return this.name === 'admin' ? '超级管理员' : '普通用户'
	    }
	  },

	  mounted: function () {
	    axios.get(this.host + 'get_year', {
	      responseType: 'json',
	      headers: {
	        'Authorization': 'JWT ' + this.token
	      },
	      withCredentials: true // 跨域带上cookies
	    })
	      .then(response => (
	        // console.log(response.data['date']),
	        this.ruleForm.year = response.data['year'],
	        this.meetingName = response.data['name'],
	        this.date = response.data['date'],
	        this.meetingNameList = response.data['meeting_list']
	      )).catch(error => {
	        // alert('error')
	        console.log(error.response.data)
	      })
	  },
	  watch: {

	  },
	  // created() {
	  //     this.handleListener();
	  //     this.changeDate();
	  // },
	  // activated() {
	  //     this.handleListener();
	  // },
	  // deactivated() {
	  //     window.removeEventListener('resize', this.renderChart);
	  //     bus.$off('collapse', this.handleBus);
	  // },
	  methods: {
	    childByValue(childValue) {
	      this.dialogFormVisible = childValue
      }
      // addMotion () {
	    //   this.motionArray.push({})
	    // },
	    // getData (year, name) {
	    //   axios.get(this.host + 'get_detail/' + this.ruleForm.year + '/' + this.meetingName)
	    //     .then(response => (
	    //       this.res_data = response.data,
	    //       this.tableData = this.res_data.list,
	    //       // 事件总线，向BaseForm组件通信，共享数据
	    //       EventBus.$emit('addition', {
	    //         year: this.ruleForm.year,
	    //         date: this.date,
	    //         meetingName: this.meetingName,
	    //         tableData: this.tableData,
	    //         motion: this.res_data.motion,
	    //         sharehold: this.res_data.sharehold
	    //       })
	    //     )).catch(error => {
	    //       // console.log(error.response);
	    //     })
	    // },
	    // submitForm (formName) {
	    //   this.$refs[formName].validate((valid) => {
	    //     if (valid) {
	    //       this.getData()
	    //     } else {
	    //       console.log('error submit!!')
	    //       return false
	    //     }
	    //   })
	    // },
	  //   submitAdd (formName) {
	  //     console.log(formName)
	  //     this.$refs[formName].validate((valid) => {
	  //       if (valid) {
	  //         axios.post(this.host + 'add_meeting', {
	  //           meeting: this.form,
	  //           motion: this.motionArray,
	  //           gdid: this.value
	  //         }).then(response => (
	  //           this.$message.success('提交成功！'),
	  //           this.dialogFormVisible = false,
	  //           location.reload()
	  //           // EventBus.$emit('addition',{
	  //           // 	year:this.form.year,
	  //           // 	meetingName: this.form.name
	  //           // })
	  //           // this.$router.push({name:'form'})
	  //         )).catch(error => (this.$message(error.response.data.msg)))
	  //       } else {
	  //         this.$message.error('数据校验失败，请按格式填写！')
	  //       }
	  //     })
	  //   },
	  //   changeDate () {
	  //     const now = new Date().getTime()
	  //     this.data.forEach((item, index) => {
	  //       const date = new Date(now - (6 - index) * 86400000)
	  //       item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
	  //     })
    // },
	  //   addMeeting () {
	  //     this.dialogFormVisible = true
	  //     axios.get(this.host + 'get_shareholder')
	  //       .then(response => (
	  //         // console.log(response.data)
	  //         this.gddata = response.data['list']
	  //         // for(var i = 0; i <= response.data['list'].length; i++) {
	  //         // 		this.gddata.push({key: response.data['list'][i].id,	label: response.data['list'][i].name})
	  //         // }
	  //       )).catch(error => {
	  //         alert('error')
	  //         // console.log(error.response.data);
	  //       })
	  //   }
	    // handleListener() {
	    //     bus.$on('collapse', this.handleBus);
	    //     // 调用renderChart方法对图表进行重新渲染
	    //     window.addEventListener('resize', this.renderChart);
	    // },
	    // handleBus(msg) {
	    //     setTimeout(() => {
	    //         this.renderChart();
	    //     }, 200);
	    // },
	    // renderChart() {
	    //     this.$refs.bar.renderChart();
	    //     this.$refs.line.renderChart();
	    // }
	  }
	}
</script>


<style scoped>



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
</style>
