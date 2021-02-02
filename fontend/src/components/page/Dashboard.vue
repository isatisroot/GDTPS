<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="8">

				<!-- 查询与新增年度会议功能卡 -->
				<el-card shadow="hover" style="height:252px;text-align: center;">
					<div slot="header" class="clearfix">
						<span class="search-box">选择股东大会年度</span>
					</div>
          <AnnualMeeting v-on:childByValue="childByValue" :dashboard="ruleForm"></AnnualMeeting>
				</el-card>
				<!-- 点击新增button之后弹出具有填写表单功能的弹窗 -->
				<el-dialog :visible.sync="dialogFormVisible"><span slot="title" style="margin-left: 300px;font-size: 30px;">新增会议</span>
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
import AnnualMeeting from '@/components/page/AnnualMeeting'
import AddMeeting from '@/components/page/AddMeeting'
export default {
	  name: 'dashboard',
	  data () {
    return {
	      username: sessionStorage.username || localStorage.username,
	      token: sessionStorage.token || localStorage.token,
	      // res_data: {},
	      ruleForm: {
	        year: localStorage.year,
          meetingName: JSON.parse(localStorage.meetingName),
	      },
	      // tableData: [],
	      dialogFormVisible: false,

	      // yearList: [],
	      // meetingNameList: [],
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
	    childByValue (childValue) {
	      this.dialogFormVisible = childValue
    }
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
