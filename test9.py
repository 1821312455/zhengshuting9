import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():

    #pd.read_excel()函数用于读取Excel文件数据
    #'supermarket_sales.xlsx'表示Excel文件路径及名称
    #sheet_name='销售数据'表示读取名为“销售数据”的工作表的数据
    #skiprows=1表示跳过Excel中的第1行是标题
    #index_col='订单号'表示将"订单号"这一列作为返回的数据框的索引
    #最后将读取到的数据框复制给变量df


    df = pd.read_excel('supermarket_sales.xlsx',
                       sheet_name='销售数据',
                       skiprows=1,
                       index_col='订单号'
                       )
    #df['时间']取出原有的'时间'这一列，其中包含交易的完整时间字符串，如'10:25:30'
    #pd.to_datatime将'时间'列转换为datatime类型
    #format="%H:%M:%S"指定原有时间字符串的格式
    #.df.hour表示从转换后的数据框取出小时作为新列
    #最后赋值给sale_df['小时']，这样就可以得到一个包含交易小时的新列
    
    df['小时数'] = pd.to_datetime(df["时间"],format="%H:%M:%S").dt.hour
    return df

def add_siderbar_func(df):
    #创建侧边栏
    # 修复：st.siderbar 拼写错误 → st.sidebar
    with st.sidebar:
        #添加侧边栏标题
        st.header("请筛选数据:")
        #求数据框"城市"列去重复值后的值，赋值给city_unique
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "请选择城市:",
            options=city_unique,#将所有选项设置为city_unique
            default=city_unique,#第1次的默认选项为city_unique
            )
        #求数据框"顾客类型"列去重复值后的值，赋值给customer_type_unique
        customer_type_unique = df["顾客类型"].unique()
        
        customer_type = st.multiselect(
             "请选择顾客类型:",
            options=customer_type_unique,#将所有选项设置为customer_type_unique
            default=customer_type_unique,#第1次的默认选项为customer_type_unique
             )
         #求数据框"性别"列去重复值后的值，赋值给gender_unique
        gender_unique = df["性别"].unique()
        
        gender = st.multiselect(
             "请选择性别:",
            options=gender_unique,#将所有选项设置为gender_unique（原注释错误已修正）
            default=gender_unique,#第1次的默认选项为gender_unique
             )
        #query():查询方法，传入过滤条件字符串
        #@city:通过@可以使用Streamlit多选下拉按钮"城市"的值
        #@customer_type:通过@可以使用Streamlit多选下拉按钮"顾客类型"的值
        #@gender：通过@可以使用Streamlit多选下拉按钮"性别"的值
        #最后赋值给变量df_selection
        df_selection = df.query(
            "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
            )

        return df_selection

def product_line_chart(df):
    #将df按'产品类型'列分组，并计算'总价'列的和，然后按总价排序
    sales_by_product_line = (
        df.groupby(by=["产品类型"])[["总价"]].sum().sort_values(by="总价")
        )
    #使用px.bar函数生成条形图
    #- x="总价":条形图的长度表示总价
    #- y=sales_by_product_line.index:条形图的标签是产品类型
    #- orientation="h":生成横向的条形图
    #- title:设置图表标题，使用HTML标签加粗

    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
        )
    #将生成的条形图返回
    return fig_product_sales


def hour_chart(df):
    #将df按'小时数'列分组，并计算'总价'列的和
    sales_by_hour = (
        df.groupby(by=["小时数"])[["总价"]].sum()
        )
    #使用px.bar函数生成条形图
    #- x="总价":条形图的长度表示总价
    #- y=sales_by_product_line.index:条形图的标签是产品类型
    #- orientation="h":生成横向的条形图
    #- title:设置图表标题，使用HTML标签加粗
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时划分的销售额</b>",
        )
     #将生成的条形图返回
    return fig_hour_sales
    
def main_page_demo(df):
    """主界面函数"""
    #设置标题
    st.title('📊销售仪表板')
    st.markdown('***')
    #创建关键指标信息区，生成3个列容器
    left_key_col,middle_key_col,right_key_col = st.columns(3)

    #选中数据框中的"总价"列，使用sum()计算"总价"列的和，使用int()求整
    total_sales = int(df["总价"].sum())
    #选中数据框中的"评分"列，使用mean()计算"评分"列的平均值，使用round()四舍五入
    #保留1位小数
    average_rating = round(df["评分"].mean(),1)
    #对刚刚的结果再次四舍五入，只保留整数，并使用int()函数，表示就要整数，增加代码的可读性
    star_rating_string = ":star:" * int(round(average_rating,0))
    #选中数据框中的"总价"列，使用mean()计算"评分"列的平均值，使用round()四舍五入
    #保留2位小数
    average_sale_by_transaction = round(df["总价"].mean(),2)



    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ￥ {total_sales:,}")

    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")

    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ￥ {average_sale_by_transaction}")

    st.divider()#生成一个水平分割线


    #创建图标信息区，生成两个列容器
    left_chart_col,right_chart_col = st.columns(2)

    with left_chart_col:
        #生成纵向条形图
        hour_fig = hour_chart(df)
        #展示生成的Plotly图形，并设置使用父容器的宽度
        st.plotly_chart(hour_fig,use_container_width=True)

    with right_chart_col:
        #生成横向条形图
        product_fig = product_line_chart(df)
        #展示生成的Plotly图形，并设置使用父容器的宽度
        st.plotly_chart(product_fig,use_container_width=True)

def run_app():
    """启动应用"""
    #设置页面
    st.set_page_config(
        page_title="销售仪表板",#标题
        page_icon=":bar_chart:",#图标
        layout="wide"#宽布局
        )
    #将Excel中的销售数据读取到数据框中
    sale_df=get_dataframe_from_excel()
    #添加不同的多选项下拉按钮，并形成筛选后的数据框，构建筛选区
    df_selection = add_siderbar_func(sale_df)
    #构建主界面
    main_page_demo(df_selection)

if __name__=="__main__":
    #标准的Python开始程序
    run_app()
