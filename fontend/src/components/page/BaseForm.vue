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
		<!-- <ul class="button-group">

			<el-tooltip class="item" effect="dark"  placement="top">
				<span slot="content">打印建议:横向-缩放75%,勾选背景图形</span>
				<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印现场会议登记表</el-button>
			</el-tooltip>
			
			<el-button class="button" icon="el-icon-printer" @click="printVote" v-print="'#printVote'">打印表决票</el-button>
			<el-button class="button" icon="el-icon-printer"  v-print="'#printStock'">打印股东、股份数统计表</el-button>
			<el-button class="button" icon="el-icon-back" @click="goback">返回</el-button>
		</ul> -->
		<!-- </div> -->
		<div class="container">
			<!-- <div id="onSite" v-show="showOnSite"> -->
			<el-tabs v-model="message" type="border-card" @tab-click="handleTabClick">
				<el-tab-pane name="first"><span slot="label"><i class="el-icon-tickets"></i> 年度会议</span>
				<el-tooltip class="item" effect="dark"  placement="right">
					<span slot="content">打印建议:横向-缩放75%,勾选背景图形</span>
					<el-button class="button" icon="el-icon-printer" @click="printOnSite">打印现场会议登记表</el-button>
				</el-tooltip>
				<h3 align="center">佛山电器照明公司</h3>
				<h2 align="center" v-show="query.year!=''">{{query.year + query.name}}现场会议登记表</h2>

				<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header"
				 @selection-change="handleSelectionChange">

					<!-- <el-table-column type="selection"  width="55" align="center" ></el-table-column> -->
					<el-table-column label="序号" width="55" align="center" type="index">
					</el-table-column>
					<el-table-column prop="cx" label="出席" width="55">
						<template slot-scope="scope">
							<el-checkbox v-model="scope.row.checked" @change="handleCheckOneChange(scope.$index)"></el-checkbox>
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
					<el-table-column label="签名"> </el-table-column>
					<el-table-column prop="emon" label="备注"></el-table-column>
					<!-- <el-table-column prop="address" label="地址"></el-table-column> -->
					<!-- <el-table-column label="状态" align="center">
			    <template slot-scope="scope">
			        <el-tag
			            :type="scope.row.state==='成功'?'success':(scope.row.state==='失败'?'danger':'')"
			        >{{scope.row.state}}</el-tag>
			    </template>
			</el-table-column> -->
					<!-- <el-table-column prop="date" label="注册时间"></el-table-column> -->
					<!-- 编辑和删除行 -->
					
					<el-table-column label="操作" width="180" align="center" >
						<template slot-scope="scope">
							<el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
							<el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
						</template>
					</el-table-column>
					

					<!-- <el-table-column>
					<el-button type="success" icon="el-icon-printer" @click="printVoucher(index)">打印凭证</el-button>
				</el-table-column> -->

				</el-table>
				
				<div class="do-not-print-me handle-box">
					<el-button type="success" icon="el-icon-circle-plus" @click="addRow"></el-button>
					<el-button type="primary" icon="el-icon-delete" class="handle-del mr10" @click="delAllSelection">批量删除</el-button>
					<!-- filterable allow-create default-first-option clearable  既可下来菜单选择又可手动输入内容 -->
					<el-select v-model="query.year" placeholder="年份" class="handle-select mr10" filterable allow-create
					 default-first-option clearable>
						<!-- <el-option key="1" label="2020" value="2020"></el-option>
						<el-option key="2" label="2019" value="2019"></el-option> -->
						<el-option v-for="(val, id) in yearList" :key="id" :value="val"></el-option>
					</el-select>
					<!-- <el-input v-model="query.name" placeholder="会议类型" class="handle-input mr10"></el-input> -->
					<!-- <el-form-item label="会议类型" required> -->
					<el-select v-model="query.name" label="会议类型" required placeholder="请选择会议类型">
						<el-option v-for="(val, id) in meetingName" :key="id" :value="val"></el-option>
					</el-select>
					<!-- </el-form-item> -->
					<el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
				</div>
				</el-tab-pane>
			
				<!-- 对应id="onSite" -->
			<!-- </div> -->
			<el-tab-pane name="second"  ><span slot="label"><i class="el-icon-tickets"></i>预览登记凭证</span>
			<certificate :year="query.year" :name="query.name" :date="query.date" :checkedData="checkedData" ></certificate>
			</el-tab-pane>
			<el-tab-pane label="预览议案表决票" name="third">
			<vote :year="query.year" :name="query.name" :checkedData="checkedData" :motion="motion" ></vote>
			</el-tab-pane>
			<el-tab-pane label="股东,股份数统计表" name="fouth">
			<stock :query="query" :statistics="statistics" > </stock>
			</el-tab-pane>
			 </el-tabs>
			<el-dialog title="编辑" :visible.sync="editVisible" width="30%">
								 <!-- <el-form ref="form" :model="form" label-width="70px">
									<el-form-item label="人数">
										<el-input v-model="form.rs"></el-input>
									</el-form-item>
									<el-form-item label="股东类型">
										<el-input v-model="form.gdtype"></el-input>
									</el-form-item>
									<el-form-item label="股东姓名">
										<el-input v-model="form.name"></el-input>
									</el-form-item>
									<el-form-item label="股东代码卡">
										<el-input v-model="form.gddmk"></el-input>
									</el-form-item>
									<el-form-item label="身份证号">
										<el-input v-model="form.sfz"></el-input>
									</el-form-item>
									<el-form-item label="A股">
										<el-input v-model="form.frA"></el-input>
									</el-form-item>
									<el-form-item label="B股">
										<el-input v-model="form.frB"></el-input>
									</el-form-item>
									<el-form-item label="备注">
										<el-input v-model="form.bz"></el-input>
									</el-form-item>
							
								</el-form> -->
								<span slot="footer" class="dialog-footer">
									<el-button @click="editVisible = false">取 消</el-button>
									<el-button type="primary" @click="saveEdit">确 定</el-button>
								</span>
							
							</el-dialog>
		</div>
		
	</div>
</template>

<script>
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
				editVisible:false,
				message:'first',
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
				indexChecked: [],
				checkedData: [],
				rowList: [],
				statistics: {
					sumA: 0,
					sumB: 0,
					sumAChecked: 0,
					sumBChecked: 0,
					sumAStock: 0,
					sumBStock: 0,
					percentA: 0,
					percentB: 0,
				},
				motion: [],



			};
		},

		created() {
			EventBus.$on('addition', param => {

				this.tableData = param.tableData;
				this.pageTotal = this.tableData.length;
				this.query.year = param.year;
				this.query.date = param.date;
				this.query.name = param.meetingName;
				// alert("date:" + this.query.date)
			});

			// this.getData();
		},

		methods: {
			// 处理选项卡的点击事件
			handleTabClick(tab, event){
				this.handleCheckedData();
			},
			// 添加行
			addRow() {
				var newValue = {
					id: '',
					cx: '',
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
			handleCheckOneChange(index) {
				// alert('勾选的下标值：' + index )
				console.log('勾选的下标值：' + index + ' 对应值为' + this.tableData[index].gdxm)
				var flag = false;
				if (this.indexChecked.length == 0) {
					// alert('列表为空，执行添加操作')
					this.indexChecked.push(index)
				} else {
					// alert('列表不为空，开始检查有无重复')
					for (var i in this.indexChecked) {
						// alert('开始遍历第' + i + '个')
						// console.log('遍历索引列表得i：' + i)
						if (index == this.indexChecked[i]) {
							// alert('去重: index =' + index + 'i是' + i + 'this.indexChecked[i]的值是' + this.indexChecked[i])							
							this.indexChecked.splice(i, 1)
							// alert('删除后的值是：' + this.indexChecked)
							flag = true;
						}
					}
					if (!flag) {
						// alert('没有重复执行追加操作')
						this.indexChecked.push(index)
					}
				}
				// console.log('列表为：' + this.indexChecked)
			},
			handleCheckedData() {
				// var indexCheckedList = Array.from(this.indexChecked)
				if (this.checkedData == 0) {
					for (var index in this.indexChecked) {
						var i = this.indexChecked[index];
						this.checkedData.push(this.tableData[i])
					}
				}


			},
			goback() {
				
			},

			printOnSite() {
				
				Print('#onSite', {
					noPrint: '.do-not-print-me',
					onStart: function() {
						console.log('onStart', new Date())
					},
					onEnd: function() {
						console.log('onEnd', new Date())
					}
				})
			},

			// printVote() {

			// 	this.handleCheckedData();

			// },

			printStock() {
				for (var index in this.indexChecked) {
					var i = this.indexChecked[index];
					if (this.tableData[i].gzA > 0) {
						console.log(this.tableData[i].gzA)
						this.statistics.sumA += 1;
						this.statistics.sumAChecked += this.tableData[i].gzA
					} else if (this.tableData[i].gzB > 0) {
						console.log(this.tableData[i].gzB)
						this.statistics.sumB += 1;
						this.statistics.sumBChecked += this.tableData[i].gzB
					}
				};


				// 求占公司所有A股股份数百分比
				for (var i in this.tableData) {

					this.statistics.sumAStock += this.tableData[i].gzA;
					this.statistics.sumBStock += this.tableData[i].gzB
				};
				this.statistics.percentA = this.sumAChecked / this.sumAStock;
				this.statistics.percentB = this.sumBChecked / this.sumBStock;


				console.log('A股人数是：' + this.statistics.sumA + ' 股份数：' + this.statistics.sumAStock + ' B股人数: ' + this.statistics.sumB +
					' B股数是:' + this.statistics.sumBStock +
					' A百分比：' + this.statistics.percentA +
					' B百分比:' + this.statistics.percentB)
			},

			printCertificate() {
				this.handleCheckedData();
				// Print('#wrap', {
				// 	onStart: function() {
				// 		console.log('onStart', new Date())
				// 	},
				// 	onEnd: function() {
				// 		console.log('onEnd', new Date())
				// 	}
				// })
			},
			// 向后台请求详细数据
			getData() {
				// fetchData(this.query).then(res => {
				// 	console.log(res);
				// 	this.tableData = res.list;
				// 	this.pageTotal = res.pageTotal || 50;
				// });
				axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name)
					.then(response => (

						console.log(11111),
						this.query.date = response.data['date'],

						this.tableData = response.data['list'],
						// console.log(reponse.data['date']),

						this.pageTotal = this.tableData.length,
						console.log(response.data['motion']),
						this.motion = response.data['motion'],
						console.log('this.motion'+this.motion)
						

					)).catch(error => {
						// alert('errorss')
						// console.log(error.response.data);
					})
			},
			// 触发搜索按钮
			handleSearch() {
				this.$set(this.query, 'pageIndex', 1);
				this.getData();
				if (this.query.year == '2020' & this.query.name == '第一次临时大会') {
					this.show = true;
				}

			},
			// 删除操作
			handleDelete(index, row) {
				// 二次确认删除
				this.$confirm('确定要删除吗？', '提示', {
						type: 'warning'
					})
					.then(() => {
						this.$message.success('删除成功');
						this.tableData.splice(index, 1);
					})
					.catch(() => {});
			},
			// 多选操作
			handleSelectionChange(val) {
				// console.log(val)
				this.multipleSelection = val;
			},
			delAllSelection() {
				const length = this.multipleSelection.length;
				let str = '';
				this.delList = this.delList.concat(this.multipleSelection);
				for (let i = 0; i < length; i++) {
					str += this.multipleSelection[i].name + ' ';
				}
				this.$message.error(`删除了${str}`);
				this.multipleSelection = [];
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
	.el-tabs__nav {
		border-radius: 13px;
		background: #20A0FF;
	}
</style>
<style scoped>

	.button-group {
		/* font-size: 0; */
		/* Inline block elements gap - fix */
		margin: 0;
		padding: 0;
		background: rgba(0, 0, 0, .1);
		border-bottom: 1px solid rgba(0, 0, 0, .1);
		padding: 7px;
		-moz-border-radius: 7px;
		-webkit-border-radius: 7px;
		border-radius: 7px;
		/* float: right; */
	}

	.button {
		border-top: 1px solid #97f7df;
		background: #65d6b6;
		background: -webkit-gradient(linear, left top, left bottom, from(#503e9c), to(#65d6b6));
		background: -webkit-linear-gradient(top, #503e9c, #65d6b6);
		background: -moz-linear-gradient(top, #503e9c, #65d6b6);
		background: -ms-linear-gradient(top, #503e9c, #65d6b6);
		background: -o-linear-gradient(top, #503e9c, #65d6b6);
		padding: 10px 20px;
		-webkit-border-radius: 13px;
		-moz-border-radius: 13px;
		border-radius: 13px;
		-webkit-box-shadow: rgba(185, 185, 185, 1.0) 0 1px 0;
		-moz-box-shadow: rgba(152, 152, 152, 1.0) 0 1px 0;
		box-shadow: rgba(127, 127, 127, 1.0) 0 1px 0;
		text-shadow: rgba(0, 0, 0, .4) 0 1px 0;
		color: white;
		font-size: 16px;
		font-family: Helvetica, Arial, Sans-Serif;
		text-decoration: none;
		vertical-align: middle;
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


	.topDiv {
		margin-top: 20px;
		margin-bottom: 20px;
	}

	.handle-box-left {
		float: left;
		/* display: inline-block; */
		margin-bottom: 20px;
	}

	.handle-box-right {
		/* float: right; */
		/* display: inline-block; */
		margin-bottom: 20px;
		margin-top: 20px;
	}

	.handle-box {
		margin-top: 20px;
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
		margin-right: 10px;
	}

	.table-td-thumb {
		display: block;
		margin: auto;
		width: 40px;
		height: 40px;
	}
</style>
