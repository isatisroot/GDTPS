<template>
  <div>
    <p class="title1" >佛山电器照明股份有限公司</p>
    <p  class="title2" align="center">{{query.year+query.name}}议案表决投反对票、弃权票统计表</p>
    <p class="text">出现会议股东代表股数：x股， 其中B股y股。</p>
    <table class="table4" >
      <tr>
        <th rowspan="2" width="40">议案编号</th>
        <th rowspan="2" width="25">子编号</th>
        <th rowspan="2" width="300">议案主题</th>
        <th colspan="3" width="300">赞成票</th>
        <th colspan="3" width="300"></th>
        <th rowspan="2" width="40">采用累积投票</th>
      </tr>
      <tr>
        <th>股份数</th>
        <th>小计</th>
        <th>合计</th>
        <th ></th>
        <th></th>
        <th></th>
      </tr>

      <tbody v-for="(m,index) in directorMotion" :key="index">
      <!--        <tbody>-->
      <tr >
        <td rowspan="2" >1</td>
        <td rowspan="2" >1</td>
        <td rowspan="2" >{{m}}</td>
        <td><span>A股</span><input style="width: 90px" v-model.number="array1[index]" @keyup.enter="fun1(array1[index], index)"></input></td>
        <td >{{countFanA[index].count}}</td>
        <td rowspan="2" >{{countFanA[index].count + countFanB[index].count}}</td>

        <td></td>
        <td ></td>
        <td rowspan="2" ></td>
        <td rowspan="2"></td>
      </tr>
      <tr>
        <!--          <td colspan="0"></td>-->
        <!--          <td rowspan="0"></td>-->
        <!--          <td rowspan="0"></td>-->
        <td><span>B股</span><input style="width: 90px" v-model.number="array3[index]" @keyup.enter="func3(array3[index], index)"></input></td>
        <td>{{countFanB[index].count}}</td>
        <!--          <td rowspan="2"></td>-->
        <td></td>
        <td></td>
        <!--            <td></td>-->
        <!--          <td></td>-->
      </tr>
      </tbody>

      <!--        </li>-->


    </table>
    <br>
  </div>
</template>

<script>
export default {
name: "Directors",
  data: function () {
    return {
      query: {
        year: null,
        name: null
      },
      directorMotion: ['选举董事会成员1', '选举董事会成员2'],
      array1: [],
      array2: [],
      array3: [],
      array4: [],
      countFanA: [{count: null}, {count: null}, {count: null}],
      countQiA: [{count: null}, {count: null}, {count: null}],
      countFanB: [{count: null}, {count: null}, {count: null}],
      countQiB: [{count: null}, {count: null}, {count: null}]

    }
  },
  created() {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
  },
  updated () {
    this.query.year = localStorage.getItem('year')
    this.query.name = JSON.parse(localStorage.getItem('meetingName'))
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
    },
    fun1 (v, index) {
      this.countFanA[index].count += v
      this.array1[index] = null
    },
    fun2 (value, index) {
      this.countQiA[index].count += value
      this.array2[index] = null
    },
    func3 (value, index) {
      this.countFanB[index].count += value
      this.array3[index] = null
    },
    func4 (value, index) {
      this.countQiB[index].count += value
      this.array4[index] = null
    }
  }
}
</script>

<style scoped>

</style>