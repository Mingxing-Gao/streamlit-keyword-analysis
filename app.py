import streamlit as st
import pandas as pd
import re
from collections import Counter

st.set_page_config(page_title="产品关键词分析工具", layout="wide")

st.title("产品关键词分析工具")
st.write("上传Excel文件并输入核心关键词，自动分析相关词汇的评论数量统计")

# 文件上传
uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])
core_keyword = st.text_input("输入核心关键词 (例如: cat bed)")

# 列选择功能
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    columns = df.columns.tolist()
    
    title_column = st.selectbox("选择标题列", columns)
    review_column = st.selectbox("选择评论数量列", columns)
    
    if st.button("分析"):
        if not core_keyword:
            st.error("请输入核心关键词")
        else:
            with st.spinner("分析中..."):
                # 确保评论列是数值类型
                df[review_column] = pd.to_numeric(df[review_column], errors='coerce').fillna(0)
                
                # 定义产品类别关键词
                product_types = [
                    f"{core_keyword}", "cave", "house", "tent", "hideaway", "condo", "tunnel", 
                    "cushion", "pillow", "sofa", "couch", "mat", "nest", "donut", "scratcher", "tree"
                ]
                
                features = [
                    "calming", "anxiety", "washable", "machine", "orthopedic", "warming", 
                    "slip", "waterproof", "cooling", "removable", "portable", "foldable"
                ]
                
                materials = [
                    "plush", "soft", "fluffy", "fur", "sherpa", "fleece", "cozy", "luxury"
                ]
                
                targets = [
                    "indoor", "small", "puppy", "kitten", "medium", "large"
                ]
                
                # 统计函数
                def count_keywords(keywords, column):
                    result = {}
                    for _, row in df.iterrows():
                        title = str(row[column]).lower()
                        review_count = row[review_column]
                        
                        for keyword in keywords:
                            if keyword.lower() in title:
                                if keyword in result:
                                    result[keyword] += review_count
                                else:
                                    result[keyword] = review_count
                    
                    return {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
                
                # 进行统计
                product_stats = count_keywords(product_types, title_column)
                feature_stats = count_keywords(features, title_column)
                material_stats = count_keywords(materials, title_column)
                target_stats = count_keywords(targets, title_column)
                
                # 显示结果
                st.subheader("1. 产品类型变体关键词统计")
                product_df = pd.DataFrame({
                    "关键词": product_stats.keys(),
                    "评论数累计": product_stats.values()
                })
                st.dataframe(product_df)
                
                st.subheader("2. 功能特性关键词统计")
                feature_df = pd.DataFrame({
                    "关键词": feature_stats.keys(),
                    "评论数累计": feature_stats.values()
                })
                st.dataframe(feature_df)
                
                st.subheader("3. 材质特征关键词统计")
                material_df = pd.DataFrame({
                    "关键词": material_stats.keys(),
                    "评论数累计": material_stats.values()
                })
                st.dataframe(material_df)
                
                st.subheader("4. 适用对象关键词统计")
                target_df = pd.DataFrame({
                    "关键词": target_stats.keys(),
                    "评论数累计": target_stats.values()
                })
                st.dataframe(target_df)
                
                st.success("分析完成!")
