<template>
    <div>
        <div class="crumbs">
<!--            <el-breadcrumb separator="/">-->
<!--                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>-->
<!--                <el-breadcrumb-item>编辑器</el-breadcrumb-item>-->
<!--            </el-breadcrumb>-->
        </div>
        <div class="container">

        </div>

				
    </div>
	
</template>

<script>

import axios from 'axios'

export default {
  name: 'editor',
  data: function () {
    return {

    }
  },


  methods: {
    addLine () { // 添加行数
      var newValue = {
        bookname: '',
        bookborrower: '',
        bookvolume: ''
      }
      // 添加新的行数
      this.tableData.push(newValue)
    }
  }
}
</script>
<style scoped>
    .editor-btn{
        margin-top: 20px;
    }
</style>