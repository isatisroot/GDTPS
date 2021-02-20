<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-pie-chart"></i> schart图表
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
          <el-input id="barCode" v-model="barCode" style="width:50%" placeholder="此处为识别的条码号"></el-input>

          <!--          <el-col :lg="10" :md="16" :xs="24">-->
<!--            <div class="grid-content">-->
<!--              <div class="titletext">扫描</div>-->
<!--              <el-card class="box-card">-->
<!--                <video id="camera" autoplay width="300" height="485"></video>-->
<!--                <canvas id="canvas" width="800" height="800" hidden="hidden"></canvas>-->
<!--                <img id="Tagimg" style="display:none" src="" alt=""/>-->
<!--              </el-card>-->
<!--              <div style="height:20px"></div>-->
<!--              <div style="text-align:left">-->
<!--                <el-tooltip class="item" effect="light" content="读取成功" placement="right-start">-->
<!--                  <el-button type="success" icon="el-icon-check" circle @click="forgetLove"></el-button>-->
<!--                </el-tooltip>-->
<!--              </div>-->
<!--            </div>-->
<!--          </el-col>-->
           <!-- <div class="plugins-tips">
                vue-schart：vue.js封装sChart.js的图表组件。
                访问地址：
                <a
                    href="https://github.com/lin-xin/vue-schart"
                    target="_blank"
                >vue-schart</a>
            </div> -->
            <div class="schart-box">
<!--                <div class="content-title">柱状图</div>-->
                <schart class="schart" canvasId="bar" :options="options1"></schart>
            </div>
            <div class="schart-box">
<!--                <div class="content-title">折线图</div>-->
                <schart class="schart" canvasId="line" :options="options2"></schart>
            </div>
            <div class="schart-box">
<!--                <div class="content-title">饼状图</div>-->
                <schart class="schart" canvasId="pie" :options="options3"></schart>
            </div>
            <div class="schart-box">
<!--                <div class="content-title">环形图</div>-->
                <schart class="schart" canvasId="ring" :options="options4"></schart>
            </div>
        </div>
    </div>
</template>

<script>
import Schart from 'vue-schart'
export default {
  name: 'basecharts',
  components: {
    Schart
  },
  data () {
    return {
      barCode: '', // 条码
      videoobj: null, // 视频对象(全局)
      options1: {
        type: 'bar',
        title: {
          text: '各项议案表决情况统计'
        },
        legend: {
          position: 'bottom',
          bottom: 20
        },
        bgColor: '#fbfbfb',
        labels: ['关于X的议案', '关于X2的议案', '关于X3的议案'],
        datasets: [
          {
            label: '赞成票',
            fillColor: 'rgba(241,49,74,0.5)',
            data: [6500000, 6780000, 6500000]
          },
          {
            label: '反对票',
            data: [1640000, 1780000, 1900000]
          },
          {
            label: '弃权票',
            data: [1440000, 1980000, 1500000]
          }
        ]
      },
      options2: {
        type: 'line',
        title: {
          text: '股价走势图'
        },
        legend: {
          position: 'bottom',
          bottom: 20
        },
        bgColor: '#fbfbfb',
        labels: ['6日', '7日', '8日', '9日', '10日'],
        datasets: [
          {
            label: 'A股',
            data: [234, 278, 270, 190, 230]
          },
          {
            label: 'B股',
            data: [164, 178, 150, 135, 160]
          }

        ]
      },
      options3: {
        type: 'pie',
        title: {
          text: '股东出席情况'
        },
        legend: {
          position: 'left'
        },
        bgColor: '#fbfbfb',
        labels: ['广东省电子信息产业集团有限公司', '香港华晟控股有限公司', '深圳市广晟投资发展有限公司', '张学权', '张勇', '网络投票-佑昌灯光器材有限公司', '网络投票-中小股东'],
        datasets: [
          {
            data: [334, 278, 190, 235, 260, 200, 141]
          }
        ]
      },
      options4: {
        type: 'ring',
        title: {
          text: '累计投票议案表决情况'
        },
        showValue: false,
        legend: {
          position: 'bottom',
          bottom: 40
        },
        bgColor: '#fbfbfb',
        labels: ['累计投票议案1', '累计投票议案2', '累计投票议案3'],
        datasets: [
          {
            data: [1800, 600, 900]
          }
        ]
      }
    }
  },
  created() {

  },
  methods: {

    // 识别二维码


  }
}
</script>

<style scoped>
.schart-box {
    display: inline-block;
    margin: 20px;
}
.schart {
    width: 600px;
    height: 400px;
}
.content-title {
    clear: both;
    font-weight: 400;
    line-height: 50px;
    margin: 10px 0;
    font-size: 22px;
    color: #1f2f3d;
}
</style>