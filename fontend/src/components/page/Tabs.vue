<template>
	<div class="">
		<div class="crumbs">
			<el-breadcrumb separator="/">
				<el-breadcrumb-item><i class="el-icon-lx-copy"></i> 表决统计</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="container">
			<el-tabs v-model="message">
				<el-tab-pane label="议案表决票" name="first">
					<div>
						<h3 align="center">佛山电器照明公司</h3>
						<h2 align="center">2020第二次临时股东大会议案表决票</h2>
						  <el-table
						    :data="tableData"
						    border
						    style="width: 100%" align="center">
						    <el-table-column
						      prop="date"
						      label="议案编号"
						      width="180" align="center">
						    </el-table-column>
						    <el-table-column
						      prop="name"
						      label="议案主题"
						      width="380" align="center">
						    </el-table-column>
						    <el-table-column
						      prop="address"
						      label="赞成" width="180" align="center">
						    </el-table-column>
							<el-table-column
							  prop="address"
							  label="反对" width="180" align="center">
							</el-table-column>
							<el-table-column
							  prop="address"
							  label="弃权" width="180" align="center">
							</el-table-column>
							
						  </el-table>
					</div>
					<!-- <el-table :data="unread" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title">{{scope.row.title}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="date" width="180"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="primary">全部标为已读</el-button>
                    </div> -->
				</el-tab-pane>
				<el-tab-pane label="董事表决赞成票统计表" name="second">
					<div>
						<h3 align="center">佛山电器照明公司</h3>
						<h2 align="center">2020第二次临时股东大会议案表决董事表决赞成票统计</h2>
						<el-table :data="tableData" style="width: 100%" align="center">
							<el-table-column prop="date" label="议案编号" width="150" align="center">
							</el-table-column>
							<el-table-column prop="date" label="子编号" width="70" align="center">
							</el-table-column>
							<el-table-column prop="name" label="议案主题" width="200" align="center">
							</el-table-column>


							<el-table-column label="赞成票" align="center">
								<el-table-column prop="province" label="股份数" width="220" align="center">
								</el-table-column>
								<el-table-column prop="city" label="小计" width="120" align="center">
								</el-table-column>
								<el-table-column prop="address" label="合计" width="120" align="center">
								</el-table-column>
							</el-table-column>

							<el-table-column label="">
								<el-table-column prop="name" label="" width="200" align="center">
								</el-table-column>
							</el-table-column>

						</el-table>
					</div>
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
				<el-tab-pane label="反对票,弃权票统计表" name="third">
					<!-- <template v-if="message === 'third'">
						<el-table :data="recycle" :show-header="false" style="width: 100%">
							<el-table-column>
								<template slot-scope="scope">
									<span class="message-title">{{scope.row.title}}</span>
								</template>
							</el-table-column>
							<el-table-column prop="date" width="150"></el-table-column>
							<el-table-column width="120">
								<template slot-scope="scope">
									<el-button @click="handleRestore(scope.$index)">还原</el-button>
								</template>
							</el-table-column>
						</el-table>
						<div class="handle-row">
							<el-button type="danger">清空回收站</el-button>
						</div>
					</template> -->
				</el-tab-pane>
			</el-tabs>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'tabs',
		data() {
			return {
				message: 'first',
				showHeader: false,
				unread: [{
					date: '2018-04-19 20:00:00',
					title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护',
				}, {
					date: '2018-04-19 21:00:00',
					title: '今晚12点整发大红包，先到先得',
				}],
				read: [{
					date: '2018-04-19 20:00:00',
					title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
				}],
				recycle: [{
					date: '2018-04-19 20:00:00',
					title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
				}]
			}
		},
		methods: {
			// handleRead(index) {
			// 	const item = this.unread.splice(index, 1);
			// 	console.log(item);
			// 	this.read = item.concat(this.read);
			// },
			// handleDel(index) {
			// 	const item = this.read.splice(index, 1);
			// 	this.recycle = item.concat(this.recycle);
			// },
			// handleRestore(index) {
			// 	const item = this.recycle.splice(index, 1);
			// 	this.read = item.concat(this.read);
			// }
		},
		computed: {
			// unreadNum() {
			// 	return this.unread.length;
			// }
		}
	}
</script>

<style>
	.message-title {
		cursor: pointer;
	}

	.handle-row {
		margin-top: 30px;
	}

</style>
