<template>
  <div>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" >
      <el-form-item prop="year">
        <!-- .number限制输入的只能是数值 -->
        <el-input v-model.number="ruleForm.year" placeholder="请输入年份" style="width: 70%;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-select v-model="dashboard?dashboard.meetingName:ruleForm.meetingName" label="会议类型" required placeholder="请选择会议类型" style="width: 70%;">
          <el-option v-for="(val, id) in meetingNameList" :key="id" :value="val"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">
<!--          <router-link :to="'/form'">-->
            <span style="color: white;">查询</span>
<!--          </router-link>-->
        </el-button>
        <el-button type="primary" @click="addMeeting">新增</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'
import {EventBus} from '@/api/event_bus'

export default {
  name: 'AnnualMeeting',
  props: ['dashboard'],
  data () {
    // 检验方法：判断查询年度会议功能模块中输入的年份是否满足以下格式
    var checkYear = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('年份不能为空'))
      }
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('请输入数字值'))
        } else {
          if (value > 2100 || value < 2000) {
            callback(new Error('年份需大于2000，小于2100'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
    return {
      dialogFormVisible: false,
      meetingNameList: [],
      ruleForm: {
        year: null,
        meetingName: ''
      },
      rules: {
        year: [{
          validator: checkYear,
          trigger: 'blur'
        }]
      }
    }
  },
  created () {
    this.init()
  },
  watch: {
    // 侦听年度会议功能卡中的年份发生变化时立马向后台发起数据请求
    'ruleForm.year': function (newVal) {
      if (newVal) {
        // alert(this.year)
        // console.log()
        axios.get(this.host + 'get_meeting/' + newVal)
          .then(response => (
            // console.log(response.data[2020]),
            this.meetingNameList = response.data[newVal]
          )).catch(error => {
            // alert('error')
          // console.log(error.response.data);
          })
      }
    }
  },
  beforeDestroy () {
    // EventBus.$emit('addition', {
    //   year: this.ruleForm.year,
    //   meetingName: this.ruleForm.meetingName
    //
    // })
  },
  methods: {
    init () {
      axios.get(this.host + 'current').then(response => {
        this.ruleForm.year = response.data['current']['year']
        this.ruleForm.meetingName = response.data['current']['name']
        this.meetingNameList = response.data['meeting_list']
      }).catch(error => { cosole.log(error) })
    },
    getData (year, name) {
      axios.get(this.host + 'get_detail/' + this.ruleForm.year + '/' + this.meetingName)
        .then(response => {
          this.res_data = response.data,
          this.tableData = this.res_data.list
          // 事件总线，向BaseForm组件通信，共享数据
          EventBus.$emit('addition', {
            year: this.ruleForm.year,
            meetingName: this.meetingName
          })
    }).catch(error => {
        // console.log(error.response);
        })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          localStorage.setItem('year', JSON.stringify(this.ruleForm.year))
          localStorage.setItem('meetingName', JSON.stringify(this.ruleForm.meetingName))
          this.$router.push('/form')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    addMeeting () {
      this.dialogFormVisible = true
      this.$emit('childByValue', this.dialogFormVisible)
    }
  }
}
</script>

<style scoped>

</style>