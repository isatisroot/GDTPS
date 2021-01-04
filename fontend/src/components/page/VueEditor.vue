<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>
                <el-breadcrumb-item>编辑器</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="plugins-tips">
                Vue-Quill-Editor：基于Quill、适用于Vue2的富文本编辑器。
                访问地址：<a href="https://github.com/surmon-china/vue-quill-editor" target="_blank">vue-quill-editor</a>
            </div>
            <quill-editor ref="myTextEditor" v-model="content" :options="editorOption"></quill-editor>
            <el-button class="editor-btn" type="primary" @click="submit">提交</el-button>
        </div>
		<div>
			<el-table :data="tableData" style="width: 100%" border>
				<!-- <el-table-column prop="cx" label="是否出席" width="80px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.cx" type="number"></el-input>
						<el-switch v-model="form.delivery"></el-switch>
					</template>
				</el-table-column> -->
		
				<!-- <el-table-column prop="rs" label="人数" width="60px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.rs" type="number"></el-input>
					</template>
				</el-table-column> -->
		
				<el-table-column prop="gdtype" label="股东类型" width="150px">
					<template slot-scope="scope">
						<el-select placeholder="请选择">
						    <el-option key="dgd" label="大股东" value="大股东"></el-option>
						    <el-option key="dgj" label="董高监" value="董高监"></el-option>
						    <el-option key="zxg" label="中小股" value="中小股"></el-option>
						</el-select>
					</template>
				</el-table-column>
				
				<el-table-column prop="name" label="股东姓名(单位)" width="180px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.name" type="text"></el-input>
					</template>
				</el-table-column>
				
				<el-table-column prop="gddmk" label="股东代码卡" width="150px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.gddmk" type="text"></el-input>
					</template>
				</el-table-column>
				
				<el-table-column prop="sfz" label="身份证(营业执照)" width="150px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.sfz" type="text"></el-input>
					</template>
				</el-table-column>
				
				<el-table-column prop="frA" label="A股" width="150px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.frA" type="number"></el-input>
					</template>
				</el-table-column>
				
				<el-table-column prop="frB" label="B股" width="150px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.frB" type="number"></el-input>
					</template>
				</el-table-column>
				
				<el-table-column prop="bz" label="备注" width="350px">
					<template slot-scope="scope">
						<el-input v-model="scope.row.bz" type="text"></el-input>
					</template>
				</el-table-column>
		
				<el-table-column>
					<template slot-scope="scope">
						<button @click="addLine" class="addBtn" v-if="scope.$index == tableData.length - 1">
							<i class="el-icon-plus"></i>
						</button>
		
						<button v-if="tableData.length > 1" @click="handleDelete(scope.$index, scope.row)" class="del-btn" >
							<i class="el-icon-minus"></i>
						</button>
					</template>
				</el-table-column>
			</el-table>
		</div>
				
    </div>
	
</template>

<script>
    import 'quill/dist/quill.core.css';
    import 'quill/dist/quill.snow.css';
    import 'quill/dist/quill.bubble.css';
    import { quillEditor } from 'vue-quill-editor';
    export default {
        name: 'editor',
        data: function(){
            return {
				tableData:[{}],
                content: '',
                editorOption: {
                    placeholder: 'Hello World'
                }
            }
        },
        components: {
            quillEditor
        },
        methods: {
			addLine() { //添加行数
				var newValue = {
					bookname: '',
					bookborrower: '',
					bookvolume: ''
				};
				//添加新的行数
				this.tableData.push(newValue);
			},
            onEditorChange({ editor, html, text }) {
                this.content = html;
            },
            submit(){
                console.log(this.content);
                this.$message.success('提交成功！');
            }
        }
    }
</script>
<style scoped>
    .editor-btn{
        margin-top: 20px;
    }
</style>