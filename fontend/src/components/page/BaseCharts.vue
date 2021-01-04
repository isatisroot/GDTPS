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
           <!-- <div class="plugins-tips">
                vue-schart：vue.js封装sChart.js的图表组件。
                访问地址：
                <a
                    href="https://github.com/lin-xin/vue-schart"
                    target="_blank"
                >vue-schart</a>
            </div> -->
            <div class="schart-box">
                <div class="content-title">柱状图</div>
                <schart class="schart" canvasId="bar" :options="options1"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">折线图</div>
                <schart class="schart" canvasId="line" :options="options2"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">饼状图</div>
                <schart class="schart" canvasId="pie" :options="options3"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">环形图</div>
                <schart class="schart" canvasId="ring" :options="options4"></schart>
            </div>
        </div>
    </div>
</template>

<script>
import Schart from 'vue-schart';
export default {
    name: 'basecharts',
    components: {
        Schart
    },
    data() {
        return {
            options1: {
                type: 'bar',
                title: {
                    text: '参会人数统计'
                },
                bgColor: '#fbfbfb',
                labels: ['第一次临时股东大会', '第二次临时股东大会', '第三次临时股东大会'],
                datasets: [
                    {
                        label: '大股东',
                        fillColor: 'rgba(241, 49, 74, 0.5)',
                        data: [150, 278, 270]
                    },
                    {
                        label: '中小股东',
                        data: [164, 178, 190]
                    },
                    {
                        label: '董高监',
                        data: [144, 198, 150]
                    }
                ]
            },
            options2: {
                type: 'line',
                title: {
                    text: '股价走势图'
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
                    },
                    
                ]
            },
            options3: {
                type: 'pie',
                title: {
                    text: '持股占比图'
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
                    text: '关于修改《公司章程》的议案'
                },
                showValue: false,
                legend: {
                    position: 'bottom',
                    bottom: 40
                },
                bgColor: '#fbfbfb',
                labels: ['赞成', '反对', '弃权'],
                datasets: [
                    {
                        data: [500, 500, 500]
                    }
                ]
            }
        };
    }
};
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