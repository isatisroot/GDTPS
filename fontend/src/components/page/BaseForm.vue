<template>
	<div>
		<!-- <div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item>
					<i class="el-icon-lx-calendar"></i> 表单
				</el-breadcrumb-item>
				<el-breadcrumb-item>新增会议</el-breadcrumb-item>
			</el-breadcrumb>
		</div> -->
		<!-- <div class="topDiv"> -->
		<ul class="button-group">
			<div class="search-box">
				<el-select v-model="query.year" placeholder="年份" class="handle-select mr10" filterable allow-create
				 default-first-option clearable>
					
					<el-option v-for="(val, id) in yearList" :key="id" :value="val"></el-option>
				</el-select>
				
				<el-select v-model="query.name" label="会议类型" required placeholder="请选择会议类型">
					<el-option v-for="(val, id) in meetingName" :key="id" :value="val"></el-option>
				</el-select>
				
				<el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
				<el-button type="primary" icon="el-icon-circle-plus" >新增</el-button>
			</div>
			<div class="sharemsg">
				<span>总股本：</span>
				<el-input v-model="share.totalShare" :disabled="disabled"></el-input>
				<span>流通A股：</span>
				<el-input v-model="share.AShareTotal" :disabled="disabled"></el-input>
				<span>流通B股：</span>
				<el-input v-model="share.BShareTotal" :disabled="disabled"></el-input>
				<el-button type="info" @click="editTable" icon="el-icon-edit">编辑</el-button>
				<!-- <el-button type="primary" icon="el-icon-circle-plus" @click="addRow">新增行</el-button> -->
				<el-button type="success" icon="el-icon-success" @click="updateTable">保存</el-button>
				<template v-if="tab==0" >
				<el-tooltip class="item" effect="dark" placement="bottom-start">
					<!-- <el-alert title="请保存信息后再打印" type="warning" > -->
					<span slot="content" v-show="disabled">打印建议:横向-缩放61%,勾选背景图形</span>
					<span slot="content" v-show="!disabled">请保存信息后再打印</span>
					<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印</el-button>
				</el-tooltip>
				 
				  </el-alert>
				</template>
				<template v-else-if="tab == 1">
					<el-button class="button" icon="el-icon-printer"  v-print="'#printCerificate'">打印</el-button>
				</template>
				<template v-else-if="tab == 2">
					<el-button class="button" icon="el-icon-printer" v-print="'#printVote'">打印</el-button>
				</template>
				<template v-else-if="tab == 3">
					<el-button class="button" icon="el-icon-printer" v-print="'#printStock'">打印</el-button>
				</template>
			</div>
			
			<!-- <el-tooltip class="item" effect="dark"  placement="top">
				<span slot="content">打印建议:横向-缩放75%,勾选背景图形</span>
				<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印现场会议登记表</el-button>
			</el-tooltip>
			
			<el-button class="button" icon="el-icon-printer" @click="printVote" v-print="'#printVote'">打印表决票</el-button>
			<el-button class="button" icon="el-icon-printer"  v-print="'#numOfStock'">打印股东、股份数统计表</el-button>
			<el-button class="button" icon="el-icon-back" @click="goback">返回</el-button> -->
		</ul>
		<!-- </div> -->
		<div class="container">
			<!-- <div id="onSite" v-show="showOnSite"> -->
			<el-tabs v-model="message" type="border-card" @tab-click="handleTabClick" >
				<el-tab-pane  name="first"><span slot="label"><i class="el-icon-tickets"></i> 年度会议</span>

					<!-- <div class="sharemsg">
						<span>总股本：</span>
						<el-input v-model="totalShare" :disabled="disabled"></el-input>
						<span>流通A股：</span>
						<el-input v-model="AShareTotal" :disabled="disabled"></el-input>
						<span>流通B股：</span>
						<el-input v-model="BShareTotal" :disabled="disabled"></el-input>
						<el-button type="info" @click="disabled=false" icon="el-icon-edit">编辑</el-button>
						<el-button type="primary" icon="el-icon-circle-plus" @click="addRow">新增行</el-button>
						<el-button type="success" icon="el-icon-success">保存</el-button>
						<el-tooltip class="item" effect="dark" placement="left">
							<span slot="content">打印建议:横向-缩放61%,勾选背景图形</span>
							<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印</el-button>
						</el-tooltip>
					</div> -->
					<div>
						<!-- <div class="search-box">
							<el-select v-model="query.year" placeholder="年份" class="handle-select mr10" filterable allow-create
							 default-first-option clearable>
								
								<el-option v-for="(val, id) in yearList" :key="id" :value="val"></el-option>
							</el-select>
							
							<el-select v-model="query.name" label="会议类型" required placeholder="请选择会议类型">
								<el-option v-for="(val, id) in meetingName" :key="id" :value="val"></el-option>
							</el-select>
							
							<el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
						</div> -->

						<!-- <div class="do-not-print-me handle-box">
							<el-tooltip class="item" effect="dark" placement="left">
								<span slot="content">打印建议:横向-缩放61%,勾选背景图形</span>
								<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印</el-button>
							</el-tooltip>
							<el-button type="info" icon="el-icon-edit" @click="[disabled=!disabled]">{{disabled?'隐藏编辑':'编辑行'}}</el-button>
							<el-button type="primary" icon="el-icon-circle-plus" @click="addRow">新增行</el-button>
							<el-button type="success" icon="el-icon-success">更新表</el-button>

						</div> -->

					</div>
					<div id="onSite">
						<p class="title1" >佛山电器照明股份有限公司</p>
						<p class="title2"  v-show="query.year!=''">{{query.year+query.name}}现场会议登记表</p>
						<el-table :data="tableData" border class="table" ref="multipleTable" :header-cell-style="headerCellStyle"
						:cell-style="cellStyle" @selection-change="handleSelectionChange" >
							<el-table-column label="序号" width="55" align="center" type="index">
							</el-table-column>
							<el-table-column prop="cx" label="出席" width="55" >
								<template slot-scope="scope">
									<el-checkbox :disabled="disabled" v-model="scope.row.cx" @change="handleCheckOneChange(scope.$index)"></el-checkbox>
								</template>
							</el-table-column>
							<el-table-column  prop="xc" label="现场" width="55">
								<template slot-scope="scope">
									<el-checkbox :disabled="disabled" v-model="scope.row.xc"></el-checkbox>
								</template>
							</el-table-column>
							<el-table-column prop="rs" label="人数" width="55"> </el-table-column>
							<el-table-column prop="gdtype" label="股东类型" width="85"> </el-table-column>
							<el-table-column prop="gdxm" label="股东姓名(单位)" width="255">
							</el-table-column>
							<el-table-column prop="gddmk" label="股东代码卡"> </el-table-column>
							<el-table-column prop="sfz" label="身份证号码 " width="190"> </el-table-column>
							<el-table-column prop="gzA" label="A股" align="right"> </el-table-column>
							<el-table-column prop="gzB" label="B股" align="right"> </el-table-column>
							<el-table-column label="签名" align=center> </el-table-column>
							<el-table-column prop="meno" label="备注" align="center"></el-table-column>
							<el-table-column label="操作" width="180" align="center" v-if="!disabled">
								<template slot-scope="scope">
									<el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
									<el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
								</template>
							</el-table-column>
						</el-table>
					</div>

				</el-tab-pane>


				<el-tab-pane :disabled="!disabled" name="second"><span slot="label"><i class="el-icon-tickets"></i>预览登记凭证</span>
					<certificate :year="query.year" :name="query.name" :date="query.date" :checkedData="checkedData"></certificate>
				</el-tab-pane>
				<el-tab-pane :disabled="!disabled" label="预览议案表决票" name="third">
					<vote :year="query.year" :name="query.name" :checkedData="checkedData" :motion="motion"></vote>
				</el-tab-pane>
				<el-tab-pane :disabled="!disabled" label="股东,股份数统计表" name="fouth">
					<stock :share="share" :query="query" :summary = "countCheckedData">
					</stock>
				</el-tab-pane>
				
			</el-tabs>
			<el-dialog title="编辑" :visible.sync="editVisible" width="30%">
				<el-form ref="form" :model="form" label-width="90px">
					<el-form-item label="人数">
						<el-input v-model="form.rs"></el-input>
					</el-form-item>
					<el-form-item label="股东类型">
						<el-input v-model="form.gdtype"></el-input>
					</el-form-item>
					<el-form-item label="股东姓名">
						<el-input v-model="form.gdxm"></el-input>
					</el-form-item>
					<el-form-item label="股东代码卡">
						<el-input v-model="form.gddmk"></el-input>
					</el-form-item>
					<el-form-item label="身份证号">
						<el-input v-model="form.sfz"></el-input>
					</el-form-item>
					<el-form-item label="A股">
						<el-input v-model="form.gzA"></el-input>
					</el-form-item>
					<el-form-item label="B股">
						<el-input v-model="form.gzB"></el-input>
					</el-form-item>
					<el-form-item label="备注">
						<el-input v-model="form.meno"></el-input>
					</el-form-item>

				</el-form>
				<span slot="footer" class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="saveEdit">确 定</el-button>
				</span>

			</el-dialog>
		</div>

	</div>
</template>

<script>
	import {
		vm
	} from '../../main.js'
	import axios from 'axios';
	import certificate from './Certificate.vue'
	import stock from './Stocks.vue'
	import vote from './Vote.vue'
	import director from './Director.vue'
	import oppose from './Oppose.vue'
	import {
		Print
	} from "../../utils/Print.js"
	import {
		EventBus
	} from '../../api/event_bus.js';
	export default {
		name: 'baseform',
		components: {
			certificate,
			stock,
			vote,
			director,
			oppose
		},
		data() {
			var currenYear = new Date().getFullYear();
			return {
				warning:false,
				tab:0,
				headerCellStyle:{
					background:'#00dea3 !important',
					color:'#7100aa',
					'border-bottom': 'solid 1px #000000 !important',
					'border-right':'solid 1px #000000 !important',
					
					},
				cellStyle:{
					'border-bottom':'solid 1px #000000',
					'border-right':'solid 1px #000000 !important',
					
					},

				form: {

				},
				
				disabled: true,  // 为true时无法编辑
				share:{
					totalShare: 1399346154,
					AShareTotal: 1077274404,
					BShareTotal: 322071750,
				},
				
				editVisible: false,
				message: 'first',
				query: {
					address: '',
					year: '',
					name: '',
					date: null,
					pageIndex: 1,
					pageSize: 15
				},
				yearList: [currenYear, currenYear + 1],
				meetingName: ["第一次临时股东大会", "第二次临时股东大会", "第三次临时股东大会"],
				tableData: [],
				rowChecked: [], // 存储“出席”列中勾选的复选框所在行的行号（下标从0开始）
				checkedData: [],
				rowList: [],
				
				motion: [],


			};
		},

		created() {
			// 将数字转换为千位分隔符字符串
			// this.share.totalShare = String(1399346154).replace(/(\d)(?=(\d{3})+$)/g, "$1,");
			// this.share.AShareTotal = String(1077274404).replace(/(\d)(?=(\d{3})+$)/g, "$1,");
			// this.share.BShareTotal = String(322071750).replace(/(\d)(?=(\d{3})+$)/g, "$1,");
			// 处理从主页查询传过来的数据
			EventBus.$on('addition', param => {
				this.tableData = param.tableData;
				this.pageTotal = this.tableData.length;
				this.query.year = param.year;
				this.query.date = param.date;
				this.query.name = param.meetingName;
				this.motion = param.motion;
				this.initSelectData()

			});
			// console.log(this.tableData)
		},
		mounted() {
			if(!this.query.year){
				axios.get(this.host + 'get_year')
					.then(response => (
						// console.log(response.data['date']),
						this.query.year = response.data['year'],
						this.query.name = response.data['name'],
						// this.date = response.data['date'],
						this.meetingName = response.data['meeting_list']
					)).catch(error => {
						// alert('error')
						console.log(error.response.data);
					})
			}
		},
		computed:{
			countCheckedData:function(){
				var summary = {PeopleA:0, PeopleB:0, AStock:0, BStock:0, PercentA:0, PercentB:0, PercentTotal:0}
				for(var index in this.checkedData){
					var row = this.checkedData[index]
					if(row.gzA > 0){
						summary.PeopleA += row.rs
						summary.AStock += row.gzA
					}else if(row.gzB > 0){
						summary.PeopleB += row.rs
						summary.BStock += row.gzB
					}
				}
				
				summary.PercentA = this.GetPercent(summary.AStock, this.share.AShareTotal);
				summary.PercentB = this.GetPercent(summary.BStock, this.share.BShareTotal);
				summary.PercentTotal = this.GetPercent(summary.AStock+summary.BStock, this.share.totalShare);
				
				return summary
			}
		},
		methods: {
			editTable(){
				this.disabled = false;
				this.addRow()
			},
			// 处理选项卡的点击事件
			handleTabClick(tab, event) {
				if(this.disabled == false){
					this.$message.success(`请先保存当前信息`);
				}
				this.tab = tab.index
				// this.handleCheckedData();
				// 如果切换到统计表，则调用方法进行统计计算
				// if (tab.index == 3) {
				// 	this.numOfStock()
				// }
			},

			
			// 求百分比
			GetPercent(num, total) {
				num = parseFloat(num);
				total = parseFloat(total);
				if (isNaN(num) || isNaN(total)) {
					return "-";
				}
				return total <= 0 ? "0%" : (Math.round(num / total * 10000) / 100.00) + "%";
			},

			// 触发搜索按钮
			async handleSearch() {
				// 等待异步请求axios处理完成后再执行initSelectRow操作，因为后者需要等到tableData拿到数据后进行操作
				await this.getData();
				// 初始化rowChecked中的数据
				this.initSelectRow()
				this.handleCheckedData();

			},

			// 向后台请求详细数据
			getData() {
				return axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name)
					.then(response => (
						this.query.date = response.data['date'],
						this.tableData = response.data['list'],
						this.pageTotal = this.tableData.length,
						this.motion = response.data['motion']
					)).catch(error => {})

			},

			// 初始化rowChecked数据
			initSelectRow() {
				if (this.tableData) {
					for (let i = 0; i < this.tableData.length; i++) {
						if (this.tableData[i].cx == true) {
							// this.checkedData.push(this.tableData[i])
							this.rowChecked.push(i)
						}
					}
				}
			},
			
			

			// 打印现场会议登记表
			printOnSite() {
				// 现将操作列隐藏起来，以免打印这一列
				
				if(this.disabled == false){
					this.$message({
					          showClose: true,
					          message: '请保存信息后再打印',
					          type: 'warning'
					        });
				}else{
					Print('#onSite', {
						// 以下class属性的div元素不会打印
						noPrint: '.do-not-print-me',
						onStart: function() {
							console.log('onStart', new Date())
						},
						onEnd: function() {
							console.log('onEnd', new Date())
						}
					})
				}
				
			},

			// 新增行
			addRow() {
				var newValue = {
					id: '',
					cx: '',
					xc: '',
					rs: '',
					gdtype: '',
					name: '',
					gddmk: '',
					sfz: '',
					frA: '',
					frB: '',
					qm: '',
					bz: ''
				};
				this.tableData.push(newValue)
			},

			// 更新表数据
			updateTable() {
				this.disabled = true;
				this.$message.success(`数据保存成功！`);
				this.handleCheckedData();
			},

			// 当点击“出席”列的复选框时，记录点击行的行号（从0开始），存储在rowChecked中
			handleCheckOneChange(rowNum) {
				// console.log('勾选的下标值：' + row + ' 对应值为' + this.tableData[row].gdxm + '出席' + this.tableData[row].cx)
				// 当为true时将该行的行号添加追加到列表后重新排序，为false将其剔除
				if (this.tableData[rowNum].cx == true) {
					this.rowChecked.push(rowNum);
					this.rowChecked.sort(function(a, b) {
						return a - b
					})
					// console.log(this.rowChecked)
				} else {
					// console.log(this.rowChecked)
					var index = this.rowChecked.indexOf(rowNum)
					this.rowChecked.splice(index, 1)
					// console.log(this.rowChecked)					
				}

			},

			// 将存储在rowChecked列表中的行号对应的行数据添加至checkedData列表中，使其传递给子组件
			handleCheckedData() {
				console.log(this.rowChecked)
				this.checkedData = []
				// index是rowChecked的下标，
				for (var i in this.rowChecked) {
					var index = this.rowChecked[i];
					this.checkedData.push(this.tableData[index])
				}
			},

			// 编辑操作
			handleEdit(index, row) {
				this.idx = index;
				this.form = row;
				console.log(index)
				this.editVisible = true;
				
			},



			// 保存编辑
			saveEdit() {
				this.editVisible = false;
				this.$message.success(`修改第 ${this.idx + 1} 行成功`);
				this.$set(this.tableData, this.idx, this.form);
				this.addRow()
			},
			// 分页导航
			handlePageChange(val) {
				this.$set(this.query, 'pageIndex', val);
				this.getData();
			}
		}
	};
</script>
<style>
	.title1 {
		/* margin-top: 30px; */
		/* margin-bottom: 10px; */
		text-align: center;
		font-size: 36px;
		font-family: "LiSu" ;
		color:orangered;
		
	}
	.title2{
		/* margin-top: 15px; */
		/* margin-bottom: 20px; */
		line-height: 80px;
		text-align: center;
		font-size: 38px;
		color:indianred
	}
	
	.el-tabs__nav {
		/* border-radius: 13px; */
		background: #6666ff;
		/* background: -webkit-gradient(linear, left top, left bottom, from(#6666ff), to(#6666ff)); */
		/* background: -webkit-linear-gradient(top, #503e9c, #65d6b6); */
		/* background: -moz-linear-gradient(top, #503e9c, #65d6b6);
		background: -ms-linear-gradient(top, #503e9c, #65d6b6);
		background: -o-linear-gradient(top, #503e9c, #65d6b6); */
		/* padding: 10px 20px; */
		/* -webkit-border-radius: 13px;
		-moz-border-radius: 13px; */
		/* border-radius: 13px; */
		/* -webkit-box-shadow: rgba(185, 185, 185, 1.0) 0 1px 0; */
		-moz-box-shadow: rgba(152, 152, 152, 1.0) 0 1px 0;
		box-shadow: rgba(127, 127, 127, 1.0) 0 1px 0;
		/* text-shadow: rgba(0, 0, 0, .4) 0 1px 0; */
	}

	.el-tabs--border-card>.el-tabs__header .el-tabs__item {
		border: 3px solid #FFFFFF;
		border-radius: 5px;
		color: white
	}

	.el-tabs--border-card>.el-tabs__header .el-tabs__item.is-active {
		color: #3f51b5;
		/* background-color: #00BCD4; */
		background: -webkit-gradient(linear, left top, left bottom, from(#6699ff), to(#ffffff));
		border-radius: 5px;
		font-weight: 600;
	}


	.button {
		border-top: 1px solid #97f7df;
		background: #1ABC9C;
		/* margin-left: 800px; */
		/* position: absolute; */
		/* right: 50px; */
		/* top:35px; */
		/* background: -webkit-gradient(linear, left top, left bottom, from(#503e9c), to(#65d6b6)); */
		/* background: -webkit-linear-gradient(top, #503e9c, #65d6b6);
		background: -moz-linear-gradient(top, #503e9c, #65d6b6);
		background: -ms-linear-gradient(top, #503e9c, #65d6b6);
		background: -o-linear-gradient(top, #503e9c, #65d6b6); */
		padding: 9px 15px;
		/* -webkit-border-radius: 13px;
		-moz-border-radius: 13px; */
		border-radius: 3px;
		/* -webkit-box-shadow: rgba(185, 185, 185, 1.0) 0 1px 0;
		-moz-box-shadow: rgba(152, 152, 152, 1.0) 0 1px 0;
		box-shadow: rgba(127, 127, 127, 1.0) 0 1px 0; */
		/* text-shadow: rgba(0, 0, 0, .4) 0 1px 0; */
		color: white;
		font-size: 12px;
		/* font-family: Helvetica, Arial, Sans-Serif;
		text-decoration: none;
		vertical-align: middle; */
	}

	.button:hover {
		border-top-color: #287378;
		background: #287378;
		color: #ccc;
	}

	.button:active {
		border-top-color: #3162a7;
		background: #1b365c;
	}
</style>
<style scoped>
	.el-table--border:after,
	.el-table--group:after,
	.el-table:before {
	    background-color: #000000;
	}
	.el-table--border,
	.el-table--group {
	    border-color: #000000;
	}

	
	.table-header{
		background: #07C4A8;
	}
		
	
	.sharemsg {
		/* display: inline-block; */
		text-align: right;
	}

	.sharemsg .el-input {
		/* display: inline-block; */
		width: 10%;
		margin-right: 10px;
	}

	.sharemsg span {
		margin-left: 5px;
	}

	.search-box {
		margin-bottom: 20px;
		/* display: inline-block; */
		text-align: right;

	}

	.search-box .el-select {
		margin-right: 10px;
	}

	.button-group {
		/* font-size: 0; */
		/* Inline block elements gap - fix */
		margin-bottom: 10px;
		padding: 0;
		/* background: rgba(255, 170, 127, 0.1); */
		background: linear-gradient(to top, rgba(255,255,255,1), rgba(255,255,255,0));
		border-bottom: 1px solid rgba(0, 0, 0, .1);
		padding: 7px;
		-moz-border-radius: 7px;
		-webkit-border-radius: 7px;
		border-radius: 7px;
		/* float: right; */
	}


	.topDiv {
		margin-top: 20px;
		margin-bottom: 20px;
	}

	.handle-box {
		margin-top: 20px;
		display: inline-block;
		position: absolute;
		right: 16px;
	}

	.handle-select {
		width: 120px;
	}

	.handle-input {
		width: 300px;
		display: inline-block;
	}

	.table {
		width: 100%;
		font-size: 14px;

	}

	.red {
		color: #ff0000;
	}

	.mr10 {
		/* margin-right: 10px; */
	}

	.table-td-thumb {
		display: block;
		margin: auto;
		width: 40px;
		height: 40px;
	}
</style>
