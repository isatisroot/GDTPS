<template>

    <div class="login-wrap">
      <link href="https://cdn.jsdelivr.net/npm/animate.css@3.5.1" rel="stylesheet" type="text/css">
        <div class="ms-login" v-if="show">
            <div class="ms-title">佛山照明股东投票系统</div>
            <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="param.username" placeholder="请输入用户名">
                        <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        type="password"
                        placeholder="请输入密码"
                        v-model="param.password"
                        @keyup.enter.native="submitForm()"
                    >
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm()">登录</el-button>
                </div>
                <!-- <p class="login-tips">Tips : 测试阶段：用户名和密码随便填。</p> -->
            </el-form>
        </div>

        <div class="ms-login animated fadeInUp"  v-if="!show & !dialogFormVisible" style="text-align: center">
          <div class="ms-title">选择年度会议</div>

          <AnnualMeeting class="ms-content" v-on:childByValue="childByValue"></AnnualMeeting>
        </div>
      <div v-if="dialogFormVisible" class="new-meeting animated fadeInUp">
        <div class="ms-title">新增会议</div>
      <AddMeeting v-on:addValue="addMeetingValue" ></AddMeeting>
      </div>


    </div>
</template>

<script>
	import axios from 'axios'
import AnnualMeeting from '@/components/page/AnnualMeeting'
import AddMeeting from '@/components/page/AddMeeting'
export default {
  components: {
    AnnualMeeting, AddMeeting
  },
  data: function () {
    return {
      dialogFormVisible: false,
      show: true,
      param: {
        username: 'admin',
        password: '123123'
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },

  methods: {
    addMeetingValue(childValue){
      this.dialogFormVisible = childValue
    },
    childByValue (childValue) {
      this.dialogFormVisible = childValue
    },
    submitForm () {
      this.$refs.login.validate(valid => {
        if (valid) {
          // this.$router.push('/')
          axios.post(this.host + 'login', {
	            username: this.param.username,
	            password: this.param.password
	          }).then(response => {
            this.$message.success('登录成功！')
            this.show = false
            // localStorage.setItem('ms_username', this.param.username)
            localStorage.setItem('ms_username', response.data['username'])
            localStorage.setItem('token', response.data['token'])
	            // this.$router.push('/')
	          }).catch(error => {
	            this.$message.error('登录失败')
	          })
        } else {
          this.$message.error('请输入账号和密码')
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>

.login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
  background-attachment:scroll !important;
    background-image: url(../../assets/img/FSLbackground.png);
    background-size: 100%;
  background-repeat:no-repeat;

}
.ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 25px;
    color: #fff;
    border-bottom: 1px solid #ddd;
}
.ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width:350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.3);
    overflow: hidden;
}

.ms-login:hover{
	text-shadow: 0 0 0.1em, 0 0 0.3em;
}
.ms-content {
    padding: 30px 30px;
}
.login-btn {
    text-align: center;
}
.login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}
.login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
}
.new-meeting{
  position: absolute;
  left: 32%;
  top: 10%;
  overflow-y: scroll;
  /*margin: -190px 0 0 -175px;*/
  /*margin: auto;*/
  border-radius: 5px;
  width: 700px;
  height: 550px;
  background: rgba(255, 255, 255, 0.3);

}

/*控制整个滚动条*/
::-webkit-scrollbar {
  /*background-color: lightgray;*/
  width: 10px;
  height: 10px;
  background-clip: padding-box;
}

/*滚动条两端方向按钮*/
::-webkit-scrollbar-button {
  /*background-color: pink;*/
}

/*滚动条中间滑动部分*/
::-webkit-scrollbar-thumb {
  background-color: lightgray;
  border-radius: 5px;
  opacity: 0.5;
}

/*滚动条右下角区域*/
::-webkit-scrollbar-corner {
  background-color: red;
}

</style>