<template>
  <div>
    <el-form :model="form" :rules="rules" ref="form">
<!--      <el-divider style="margin-top: 10px">基本信息</el-divider>-->
      <el-form-item label="会议名称" prop="name" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" style="width: 80%"></el-input>
      </el-form-item>

      <el-form-item label="会议时间" :label-width="formLabelWidth" required>
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
      <el-form-item prop="address" label="会议地点" :label-width="formLabelWidth" default-first-option>
        <!-- <el-cascader :options="options" v-model="form.address"></el-cascader> -->
        <el-input v-model="form.address" style="width: 80%"></el-input>
      </el-form-item>
      <el-divider style="margin-top: 10px">议案主题</el-divider>
      <div style="text-align: center;margin-top: -10px;margin-bottom: 15px">

        <span style="font-size: 10px;color:orangered;background: white">(✔表示采用累积投票)</span>
      </div>
      <el-form-item  :label-width="formLabelWidth">
        <!-- <template slot-scope="scope"> -->
        <div style="float: left; width: 80%">
          <!-- <li v-for="(val, id) in motion.list" :key="id" style="list-style-type:none;">
            <el-input type="text" style="margin-bottom: 5px;" v-model="val.text"></el-input>
          </li> -->
          <!-- 使用作用域插槽，el-table是子组件，现在往子组件传<template>的内容，并获取里面的内容 -->
          <el-table :data="motionArray" :show-header="false" ref="multipleTable" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="28px"></el-table-column>
            <el-table-column prop=motion>
              <template slot-scope="scope">
                <el-input v-model="motionArray[scope.$index].motion"></el-input>
              </template>
            </el-table-column>
<!--            <el-table-column></el-table-column>-->
          </el-table>
          <!-- <el-input type="text" style="margin-bottom: 5px;"></el-input>
          <el-input type="text" style="margin-bottom: 5px;"></el-input> -->
        </div>
<!--        <div style="float:right">-->
<!--          <el-button style="height: 32px;margin-top: 8px" icon="el-icon-circle-plus" type="success" @click="addMotion"></el-button>-->
<!--        </div>-->
        <!-- </template> -->
      </el-form-item>
<!--      <el-form-item label="累计投票议案" :label-width="formLabelWidth">-->
<!--        &lt;!&ndash; <template slot-scope="scope"> &ndash;&gt;-->
<!--        <div style="float: left; width: 90%">-->
<!--          &lt;!&ndash; <li v-for="(val, id) in motion.list" :key="id" style="list-style-type:none;">-->
<!--            <el-input type="text" style="margin-bottom: 5px;" v-model="val.text"></el-input>-->
<!--          </li> &ndash;&gt;-->
<!--          &lt;!&ndash; 使用作用域插槽，el-table是子组件，现在往子组件传<template>的内容，并获取里面的内容 &ndash;&gt;-->
<!--          <el-table :data="leijimotionArray" :show-header="false">-->
<!--            <el-table-column prop=motion>-->
<!--              <template slot-scope="scope">-->
<!--                <el-input v-model="leijimotionArray[scope.$index].motion"></el-input>-->
<!--              </template>-->
<!--            </el-table-column>-->
<!--            &lt;!&ndash;            <el-table-column></el-table-column>&ndash;&gt;-->
<!--          </el-table>-->
<!--          &lt;!&ndash; <el-input type="text" style="margin-bottom: 5px;"></el-input>-->
<!--          <el-input type="text" style="margin-bottom: 5px;"></el-input> &ndash;&gt;-->
<!--        </div>-->
<!--        <div style="float:right">-->
<!--          <el-button style="height: 32px;margin-top: 8px" icon="el-icon-circle-plus" type="success" @click="addleijiMotion"></el-button>-->
<!--        </div>-->
<!--        &lt;!&ndash; </template> &ndash;&gt;-->
<!--      </el-form-item>-->
      <div class="demo-block-control" @click="addMotion">
        <!--            <el-tooltip class="item" effect="dark" content="新增议案" placement="bottom">-->
        <!--            <img src="../../assets/img/toggle_bg.png" width="500px" @click="addMotion" ></img>-->

        <div class="add-motion" >
          <i class="el-icon-caret-bottom"></i>
          <span >新增议案</span>
        </div>

        <!--            </el-tooltip>-->
      </div>
      <el-divider style="margin-top: 10px">议案说明</el-divider>
      <el-form-item :label-width="formLabelWidth">
        <el-input type="textarea" :rows="2" placeholder="可选填" v-model="descr" style="margin:0 auto !important;width: 80%"></el-input>
      </el-form-item>
    </el-form>
    <div class="edit_dev">
      <el-row>
        <el-col>

          <el-transfer v-model="value" :data="gddata" :titles="['可添加股东信息列表', '已添加股东信息列表']"></el-transfer>
        </el-col>
      </el-row>

    </div>

    <div slot="footer" class="dialog-footer">
      <el-button @click="FormVisible">取 消</el-button>
      <el-button type="primary" @click="submitAdd('form')">确 定</el-button>
      <!-- <el-button type="primary">
        <router-link :to="'/table'"><span style="color: white;">确定</span></router-link>
      </el-button> -->
    </div>
  </div>

</template>

<script>
import axios from '_axios@0.18.1@axios'

export default {
  name: 'AddMeeting',
  data () {
    return {
      dialogFormVisible: true,
      rules: {

        name: [{
          required: true,
          message: '请输入会议名称',
          trigger: 'blur'
        },
        {
          min: 1,
          max: 25,
          message: '长度在1 到 25 个字符',
          trigger: 'blur'
        }
        ],
        address: [{
          required: true,
          trigger: 'blur',
          message: '请输入会议地址'
        } ],
        date0: [{

          // required: true,
          message: '请选择日期',
          trigger: 'change'
        }],
        date2: [{

          required: true,
          message: '请选择时间',
          trigger: 'change'
        }]
      },
      gddata: [],
      motionArray: [{}],
      leijimotionArray: [{}],
      descr: '',
      formLabelWidth: '120px',
      date: null,
      form: {
        name: '',
        date1: '',
        date2: '',
        options: [],
        address: '办公楼五楼会议室（佛山市禅城区汾江北路64号）',
        motion: ''
      },
      value: []
    }
  },
  created () {
    axios.get(this.host + 'get_shareholder')
      .then(response => (
        // console.log(response.data)
        this.gddata = response.data['list']
        // for(var i = 0; i <= response.data['list'].length; i++) {
        // 		this.gddata.push({key: response.data['list'][i].id,	label: response.data['list'][i].name})
        // }
      )).catch(error => {
        alert('error')
      // console.log(error.response.data);
      })
  },
  methods: {
    handleSelectionChange (val) {
      // console.log(val)
      this.multipleSelection = val
    },
    FormVisible () {
      this.dialogFormVisible = false
      this.$emit('addValue', this.dialogFormVisible)
    },
    addMotion () {
      this.motionArray.push({})
    },
    addleijiMotion () {
      this.leijimotionArray.push({})
    },
    submitAdd (formName) {
      console.log(formName)
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post(this.host + 'add_meeting', {
            meeting: this.form,
            motion: this.motionArray,
            leijimotion: this.multipleSelection,
            gdid: this.value,
            descr: this.descr
          }).then(response => (
            this.$message.success('提交成功！'),
            this.dialogFormVisible = false,
            localStorage.setItem('year', this.form.date1.substr(0, 4)),
            localStorage.setItem('meetingName', JSON.stringify(this.form.name)),
            this.$router.push({name: 'form'})
          )).catch(error => (this.$message(error.response.data.msg)))
        } else {
          this.$message.error('数据校验失败，请按格式填写！')
        }
      })
    },
    changeDate () {
      const now = new Date().getTime()
      this.data.forEach((item, index) => {
        const date = new Date(now - (6 - index) * 86400000)
        item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
      })
    }

  }
}
</script>

<style scoped>
/*/deep/ .el-table .cell, .el-table--border td:first-child .cell, .el-table--border th:first-child .cell{*/
/*  padding-left: 0px;*/
/*}*/
.edit_dev {
  margin: 0 auto;
  text-align: center;
}
.edit_dev>>>.el-transfer-panel {
  /*position: absolute;*/
  /*left: 5%;*/
  /* width: 300px;*/
  margin: 0 auto;
  width: 35%;
  text-align: left;

}
.dialog-footer{
  margin-top: 5px;
  text-align: center;
}


.demo-block-control {
  padding-top: 3px;
  border: 1px solid #eaeefb;
  height: 24px;
  box-sizing: border-box;
  background: linear-gradient(to bottom, #bbb8b8, #f5f2f1);
  border-radius: 5px;
  width: 70%;
  opacity: 0.7;
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
  color: gray;
  transition: .5s;
}
.demo-block-control:hover .add-motion i{
  color: black;
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
