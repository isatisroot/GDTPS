<template>
  <div>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="demo-ruleForm">
      <el-form-item prop="year">
        <!-- .number限制输入的只能是数值 -->
        <el-input v-model.number="ruleForm.year" placeholder="请输入年份" style="width: 50%;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-select v-model="meetingName" label="会议类型" required placeholder="请选择会议类型" style="width: 50%;">
          <el-option v-for="(val, id) in meetingNameList" :key="id" :value="val"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">
          <router-link :to="'/form'"><span style="color: white;">查询</span></router-link>
        </el-button>
        <el-button type="primary" @click="addMeeting">新增</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'AnnualMeeting',
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
      ruleForm: {
        year: null
      },
      rules: {
        year: [{
          validator: checkYear,
          trigger: 'blur'
        }]
      }
    }
  }
}
</script>

<style scoped>

</style>