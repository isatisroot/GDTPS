<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>
                <el-breadcrumb-item>markdown编辑器</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <!-- <div class="plugins-tips">
                mavonEditor：基于Vue的markdown编辑器。
                访问地址：<a href="https://github.com/hinesboy/mavonEditor" target="_blank">mavonEditor</a>
            </div> -->
            <mavon-editor v-model="content" ref="md" @imgAdd="$imgAdd" @change="change" style="min-height: 600px"/>
            <el-button class="editor-btn" type="primary" @click="submit">提交</el-button>
          <el-table :data="tableData" style="width: 100%" border>
            <!--             <el-table-column prop="cx" label="是否出席" width="80px">-->
            <!--              <template slot-scope="scope">-->
            <!--                <el-input v-model="scope.row.cx" type="number"></el-input>-->
            <!--                <el-switch v-model="form.delivery"></el-switch>-->
            <!--              </template>-->
            <!--            </el-table-column>-->

            <el-table-column prop="rs" label="人数" width="60px">
              <template slot-scope="scope">
                <el-input v-model="scope.row.rs" type="number"></el-input>
              </template>
            </el-table-column>

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
                <el-input v-model="scope.row.gdxm" type="text"></el-input>
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
                <el-input v-model="scope.row.gzA" type="number"></el-input>
              </template>
            </el-table-column>

            <el-table-column prop="frB" label="B股" width="150px">
              <template slot-scope="scope">
                <el-input v-model="scope.row.gzB" type="number"></el-input>
              </template>
            </el-table-column>

            <el-table-column prop="bz" label="备注" width="350px">
              <template slot-scope="scope">
                <el-input v-model="scope.row.meno" type="text"></el-input>
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
    import { mavonEditor } from 'mavon-editor'
    import 'mavon-editor/dist/css/index.css'
    import axios from '_axios@0.18.1@axios'
export default {
      name: 'markdown',
      data: function () {
        return {
          tableData: [{}],
          content: '',
          html: '',
          configs: {
          }
        }
      },
      components: {
        mavonEditor
      },
      mounted () {
        axios.get(this.host + 'current').then(response => {
          this.tableData = response.data['detail_list']
        })
      },
      methods: {
        // 将图片上传到服务器，返回地址替换到md中
        $imgAdd (pos, $file) {
          var formdata = new FormData()
          formdata.append('file', $file)
          // 这里没有服务器供大家尝试，可将下面上传接口替换为你自己的服务器接口
          this.$axios({
            url: '/common/upload',
            method: 'post',
            data: formdata,
            headers: { 'Content-Type': 'multipart/form-data' }
          }).then((url) => {
            this.$refs.md.$img2Url(pos, url)
          })
        },
        change (value, render) {
          // render 为 markdown 解析后的结果
          this.html = render
        },
        submit () {
          console.log(this.content)
          console.log(this.html)
          this.$message.success('提交成功！')
        }
      }
    }
</script>
<style scoped>
    .editor-btn{
        margin-top: 20px;
    }
</style>