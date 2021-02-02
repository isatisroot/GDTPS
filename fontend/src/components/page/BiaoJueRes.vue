<template>
  <div id="res1">
    <p class="title1" >佛山电器照明股份有限公司</p>
    <p  class="title2" align="center">{{query.year+query.name}}议案投票表决统计结果</p>
    <p>一、会议的出席情况</p>
    <p>1.出席的总体情况：</p>
    <p>股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>其中,现场会议股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>网络投标股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>2.A股股东出席情况：</p>
    <p>A股股东（代理人）{}人，代表股份{}股，占公司A股股东表决权股份{}%。</p>
    <p>其中,现场会议股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>网络投标股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>3.B股股东出席情况：</p>
    <p>B股股东（代理人）{}人，代表股份{}股，占公司B股股东表决权股份{}%。</p>
    <p>其中,现场会议股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>网络投标股东（代理人）{}人，代表股份{}股，占公司有表决权总股份{}%。</p>
    <p>4.中小股出席情况：</p>
    <p>中小股东（代理人）（不含公司董事、监事、高管、单独或合计持有公司5%以上股份的股东及与
      持有公司5%以上股份股东形成一致行动人的股东）共{}人，代表股份{}股，占公司B股股东表决权股份{}%。</p>
    <p>二、提案审议和表决情况</p>
    <el-divider></el-divider>
    <p>总的表决情况：同意{}股，占出席会议所有股东所持表决权{}%；反对{}股，占出席会议所有股东所持表决权{}%；
    弃权{}股，占出席会议所有股东所持表决权{}%</p>
    <p>A股股东表决情况：同意{}股，占出席会议A股东所持表决权{}%；反对{}股，占出席会议A股东所持表决权{}%；
      弃权{}股，占出席会议A股股东所持表决权{}%</p>
    <p>B股股东表决情况：同意{}股，占出席会议B股东所持表决权{}%；反对{}股，占出席会议A股东所持表决权{}%；
      弃权{}股，占出席会议B股股东所持表决权{}%</p>
    <p>表决结果：</p>
  </div>
</template>

<script>
export default {
  name: 'BiaoJueRes',
  data () {
    return{
      query: {
        year: '',
        name: ''
      }
    }
  },
  created () {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
  },
  mounted () {

  },
  updated () {
    // 当有更新时重新读取
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
  }
}
</script>

<style scoped>

</style>