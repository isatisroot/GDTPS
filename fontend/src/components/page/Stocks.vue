<template>
	<div>
		<!-- <el-button class="button" icon="el-icon-printer" v-print="'#printStock'">打印</el-button> -->
	
		<div id="printStock">
		<p class="title1" >佛山电器照明股份有限公司</p>
		<p  class="title2" align="center">{{query.name}}股东、股份数统计表</p>
		<p class="text">公司总股本：{{share.totalShare}}股，其中A股：{{share.AShareTotal}}股，B股：{{share.BShareTotal}}股</p>
		<table class="table4">
			<tr>
				<th></th>
				<th>股东人数</th>
				<th>代表股份数</th>
				<th>占股份%</th>
				<th>备注</th>
			</tr>
			<tr>
				<td>A股</td>
				<td>{{summary.PeopleA}}</td>
				<td>{{summary.AStock}}</td>
				<td>{{summary.PercentA}}</td>
				<td>占公司A股总数%</td>
			</tr>
			<tr>
				<td>B股</td>
				<td>{{summary.PeopleB}}</td>
				<td>{{summary.BStock}}</td>
				<td>{{summary.PercentB}}</td>
				<td>占公司B股总数%</td>
			</tr>
			<tr>
				<td>合计</td>
				<td>{{summary.PeopleB + summary.PeopleA}}</td>
				<td>{{summary.BStock + summary.AStock}}</td>
				<td>{{summary.PercentTotal}}</td>
				<td>占公司总股本%</td>
			</tr>
		</table>
		<br>
		<p align="right" class="bottom-p">统计人签字：____________</p>
		<p class="bottom-p"> 注：统计截止时间为{{meetingTime.t1}}，请在{{meetingTime.t2}}前送到主席台</p>
		<p align="right" class="bottom-p">佛山电器照明股份有限公司</p>
		<p align="right" class="bottom-p">{{currentDate}}</p>
	</div>
	</div>
</template>

<script>
	export default {
	  name: 'stock',
	  props: ['query', 'summary', 'share'],
	  data () {
	    return {
	      currentDate: this.dateToString()
	    }
	  },
	  computed: {
	    meetingTime: function () {
	      // 根据会议召开时间计算出统计截至时间和递交主席台时间（统计截至时间是召开前5分钟，递交时间是召开前2分钟）
	      var time = {}
	      if (this.query.date) {
	        var datetimeArray = this.query.date.split(' ')
	        var timeArray = datetimeArray[1].split(':')
        var _min = parseInt(timeArray[1]) // 会议召开时间
        var _time = timeArray[0]
        var min1 = 0 // 统计截至时间
        var min2 = 0 // 递交时间
        var time1 = ''
        var time2 = ''
        //  如果会议召开时间大于2分小于5分，分别计算min1和min2
        if (2 <= _min & _min < 5) {
	          min1 = 60 + _min - 5
          min2 = _min - 2
          time1 = _time - 1 + ':' + min1
          time2 = _time + ':' + min2
        } else if (_min < 2) {
          min1 = 60 + _min - 5
          min2 = 60 + _min - 2
          time1 = _time - 1 + ':' + min1
          time2 = _time - 1 + ':' + min2
        } else {
          min1 = _min - 5
          min2 = _min - 2
          time1 = _time + ':' + min1
          time2 = _time + ':' + min2
        }
	        time = {t1: time1, t2: time2}
	      } else {
	        time = {t1: '', t2: ''}
	      }
	      return time
	    }
	
	  },
	  methods: {
	    dateToString () {
	      var _date = new Date()
	      var year = _date.getFullYear()
	      var month = _date.getMonth() + 1
	      var day = _date.getDate()
	      var currentDate = year.toString() + '-' + month.toString() + '-' + day.toString()
	      return currentDate
	    }
	  }
	
	}
</script>

<style>

</style>
