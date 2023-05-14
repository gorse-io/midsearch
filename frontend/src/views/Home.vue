<template>
    <v-container>
        <v-card>
            <v-card-item>
                <v-chart class="chart" :option="option" />
            </v-card-item>
        </v-card>
    </v-container>
</template>

<script>
import axios from 'axios';

import { use } from "echarts/core";
import {
    TitleComponent,
    ToolboxComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from "vue-echarts";
import { ref } from "vue";

export default {
    components: {
        VChart
    },
    data() {
        return {
            option: ref({
                title: {
                    text: 'Answer Quality'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                legend: {
                    data: ['Accept', 'Reject', 'TBD']
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Accept',
                        type: 'line',
                        stack: 'Total',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: [],
                        itemStyle: { color: 'green' },
                    },
                    {
                        name: 'Reject',
                        type: 'line',
                        stack: 'Total',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: [],
                        itemStyle: { color: 'red' },
                    },
                    {
                        name: 'TBD',
                        type: 'line',
                        stack: 'Total',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: [],
                        itemStyle: { color: 'orange' },
                    }
                ]
            })
        }
    },
    setup() {
        use([
            TitleComponent,
            ToolboxComponent,
            TooltipComponent,
            GridComponent,
            LegendComponent,
            LineChart,
            CanvasRenderer,
            UniversalTransition
        ]);
    },
    mounted() {
        axios.get('/api/quality/').then((response) => {
            this.option.xAxis[0].data = response.data[0];
            this.option.series[0].data = response.data[1];
            this.option.series[1].data = response.data[2];
            this.option.series[2].data = response.data[3];
        }).catch((error) => {
            console.log(error);
        });
    }
}
</script>

<style scoped>
.chart {
    height: 400px;
}
</style>
