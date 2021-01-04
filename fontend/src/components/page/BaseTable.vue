<template>
	<div>
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item>
					<i class="el-icon-lx-cascades"></i> <!-- 股权登记统计 -->
				</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<el-tabs v-model="message" type="border-card" @tab-click="test">
				<!-- Tab选项卡第一页 -->
				<el-tab-pane name="first"><span slot="label"><i class="el-icon-tickets"></i> 年度会议</span>
					<!-- 功能选项按钮行 -->
						
						<div class="handle-box-right">
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
					<!-- 表格数据展示 -->
					<div class="handle-box">
						<h3 align="center">佛山电器照明公司</h3>
						<h2 align="center">{{query.year + query.name}}现场会议登记表</h2>
					</div>
						
						<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header"
						 @selection-change="handleSelectionChange"  :row-class-name="tableRowClassName" >
							
							<!-- <el-table-column type="selection"  width="55" align="center" ></el-table-column> -->
							<el-table-column label="序号" width="55" align="center" type="index">
							</el-table-column>
							<el-table-column  prop="cx" label="出席" width="55">
								<template slot-scope="scope">
									<el-checkbox  v-model="scope.row.checked" @change="handleCheckOneChange(scope.$index)"></el-checkbox>
								</template>
								
							</el-table-column>
							<el-table-column prop="rs" label="人数" width="55"> </el-table-column>
							<el-table-column prop="gdtype" label="股东类型" width="85"> </el-table-column>
							<el-table-column prop="gdxm" label="股东姓名(单位)" width="255">
							</el-table-column>
							<el-table-column prop="gddmk" label="股东代码卡"> </el-table-column>
							<el-table-column prop="sfz" label="身份证号码 " width="165"> </el-table-column>
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
							<el-table-column label="操作" width="180" align="center">
								<template slot-scope="scope">
									<el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
									<el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
								</template>
							</el-table-column>
							<!-- <el-table-column>
								<el-button type="success" icon="el-icon-printer" @click="printVoucher(index)">打印凭证</el-button>
							</el-table-column> -->
							
						</el-table>
					<div class="handle-box-left">
						<el-button type="success" icon="el-icon-circle-plus" @click="addRow">新增</el-button>
									
					</div>
					<!-- 显示分页 -->
					<div class="pagination">
						<el-pagination background layout="total, prev, pager, next" :current-page="query.pageIndex" :page-size="query.pageSize"
						 :total="pageTotal" @current-change="handlePageChange"></el-pagination>
					</div>
				</el-tab-pane>


				<el-tab-pane name="second" @click="test" ><span slot="label" style="background: #2eff70;"><i class="el-icon-tickets"></i>预览登记凭证</span>
					<certificate :year="query.year" :name="query.name" :date="query.date" :content="rowList"></certificate>
				</el-tab-pane>

				<el-tab-pane label="预览议案表决票" name="third">
					<vote :year="query.year" :name="query.name" :content="rowList"></vote>
				</el-tab-pane>

				<el-tab-pane label="股东,股份数统计表" name="fouth">
					<stock :year="query.year" :name="query.name"></stock>
				</el-tab-pane>


				<el-tab-pane label="董事表决赞成票统计表" name="fifth">
					<director></director>
					<!-- <template v-if="message === 'second'">
			            <el-table :data="read" :show-header="false" style="width: 100%">
			                <el-table-column>
			                    <template slot-scope="scope">
			                        <span class="message-title">{{scope.row.title}}</span>
			                    </template>
			                </el-table-column>
			                <el-table-column prop="date" width="150"></el-table-column>
			                <el-table-column width="120">
			                    <template slot-scope="scope">
			                        <el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>
			                    </template>
			                </el-table-column>
			            </el-table>
			            <div class="handle-row">
			                <el-button type="danger">删除全部</el-button>
			            </div>
			        </template> -->

				</el-tab-pane>
				<el-tab-pane label="反对票,弃权票统计表" name="sixth">
					<oppose></oppose>
				</el-tab-pane>
				<!-- <el-tab-pane label="统计表" name="seventh">
					<abstention></abstention>
				</el-tab-pane> -->
				
			</el-tabs>


		</div>

		<!-- 编辑弹出框 -->
		<el-dialog title="编辑" :visible.sync="editVisible" width="30%">
			<el-form ref="form" :model="form" label-width="70px">
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

			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button @click="editVisible = false">取 消</el-button>
				<el-button type="primary" @click="saveEdit">确 定</el-button>
			</span>

		</el-dialog>
	</div>
</template>
<!-- <script src="../../utils/Print.js"></script> -->
<script>
	import {
		EventBus
	} from '../../api/event_bus.js';
	import axios from 'axios';
	import {
		Print
	} from "../../utils/Print.js"
	import {
		fetchData
	} from '../../api/index';
	import abstention from './Abstention.vue'
	import certificate from './Certificate.vue'
	import stock from './Stocks.vue'
	import vote from './Vote.vue'
	import director from './Director.vue'
	import oppose from './Oppose.vue'
	export default {
		name: 'basetable',
		components: {
			abstention, certificate,stock, vote, director, oppose
		},
		data() {
			var currenYear = new Date().getFullYear();
			return {
				
				rowList:[],
				message: 'first',
				checked: true,
				query: {
					address: '',
					year: '',
					name: '',
					date:null,
					pageIndex: 1,
					pageSize: 15


				},
				yearList: [currenYear, currenYear - 1, currenYear + 1],
				meetingName: ["第一次临时股东大会", "第二次临时股东大会"],
				tableData: [],
				multipleSelection: [],
				delList: [],
				editVisible: false,
				pageTotal: 0,
				form: {},
				idx: -1,
				id: -1,
				checkedIndex:[],
			};
		},
		created() {
			EventBus.$on('addition', param => {
				
				this.tableData = param.tableData;
				this.pageTotal = this.tableData.length;
				this.query.year = param.year;
				this.query.date = param.date;
				this.query.name = param.meetingName;
				alert("date:" +this.query.date)
			});
			
			// this.getData();
		},
		// mounted: function() {
		// 	alert('mounted')
		// 	this.getData();
		// },
		methods: {
			test(){
				// 生成股份数统计表数据
				
			},
			handleCheckOneChange(val){
				console.log(val)
				this.checkedIndex.push(val)
			},
			tableRowClassName(row){
				// console.log(row.rowIndex)
			},
			select(row){
				this.rowList = row
			},
			// 打印凭证
			printVoucher() {
				// console.log(this.rowList)
				Print('#wrap', {
					onStart: function() {
						console.log('onStart', new Date())
					},
					onEnd: function() {
						console.log('onEnd', new Date())
					}
				})
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
			// 获取 easy-mock 的模拟数据
			getData() {
				// fetchData(this.query).then(res => {
				// 	console.log(res);
				// 	this.tableData = res.list;
				// 	this.pageTotal = res.pageTotal || 50;
				// });
				axios.get(this.host + 'get_detail/' + this.query.year + '/' + this.query.name)
					.then(response => (
						this.tableData = response.data,
						this.pageTotal = 15
					)).catch(error => {
						alert('error')
						console.log(error.response.data);
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

<style scoped>
	.handle-box-left {
		float: left;
		display: inline-block;
		margin-bottom: 20px;
	}

	.handle-box-right {
		float: right;
		display: inline-block;
		margin-bottom: 20px;
	}

	.handle-box {
		margin-bottom: 20px;
		/* float:right */
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
