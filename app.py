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
                
                # 添加关键词映射字典
                # 1. 产品类型映射
                product_type_mapping = {
                    core_keyword: {"chinese": "核心产品", "description": "基础产品类型"},
                    "cave": {"chinese": "洞/窝洞", "description": "半封闭式设计"},
                    "house": {"chinese": "屋", "description": "结构化设计"},
                    "tent": {"chinese": "帐篷", "description": "帐篷式设计"},
                    "hideaway": {"chinese": "藏身处", "description": "提供隐私的设计"},
                    "condo": {"chinese": "公寓", "description": "多层结构设计"},
                    "tunnel": {"chinese": "隧道", "description": "隧道式设计"},
                    "cushion": {"chinese": "垫", "description": "垫式设计"},
                    "pillow": {"chinese": "枕头", "description": "枕式设计"},
                    "sofa": {"chinese": "沙发", "description": "沙发式设计"},
                    "couch": {"chinese": "长椅", "description": "长椅式设计"},
                    "mat": {"chinese": "垫子", "description": "薄垫式设计"},
                    "nest": {"chinese": "巢", "description": "巢状设计"},
                    "donut": {"chinese": "甜甘圈", "description": "圆形带高边设计"},
                    "scratcher": {"chinese": "抓板", "description": "带抓板功能设计"},
                    "tree": {"chinese": "爬架", "description": "带攀爬功能设计"}
                }
                
                # 2. 功能特性映射
                feature_mapping = {
                    "calming": {"chinese": "舒缓", "description": "减轻焦虑的设计"},
                    "anxiety": {"chinese": "防焦虑", "description": "缓解焦虑感的设计"},
                    "washable": {"chinese": "可洗", "description": "可清洗的设计"},
                    "machine": {"chinese": "机洗", "description": "可机器清洗"},
                    "orthopedic": {"chinese": "骨科", "description": "提供关节支撑功能"},
                    "warming": {"chinese": "保暖", "description": "保温功能设计"},
                    "slip": {"chinese": "防滑", "description": "底部防滑设计"},
                    "waterproof": {"chinese": "防水", "description": "防水功能设计"},
                    "cooling": {"chinese": "降温", "description": "夏季降温设计"},
                    "removable": {"chinese": "可拆卸", "description": "可拆卸清洗的设计"},
                    "portable": {"chinese": "便携", "description": "易于携带的设计"},
                    "foldable": {"chinese": "可折叠", "description": "可折叠存储的设计"}
                }
                
                # 3. 材质特征映射
                material_mapping = {
                    "plush": {"chinese": "毛绒", "description": "绒毛材质"},
                    "soft": {"chinese": "柔软", "description": "柔软舒适的材质"},
                    "fluffy": {"chinese": "蓬松", "description": "松软的表面材质"},
                    "fur": {"chinese": "皮毛", "description": "皮毛材质"},
                    "sherpa": {"chinese": "绵羊绒", "description": "绵羊绒材质"},
                    "fleece": {"chinese": "摇粒绒", "description": "摇粒绒材质"},
                    "cozy": {"chinese": "舒适", "description": "提供舒适感的材质"},
                    "luxury": {"chinese": "豪华", "description": "高质感材料"}
                }
                
                # 4. 适用对象映射
                target_mapping = {
                    "indoor": {"chinese": "室内", "description": "适合室内饲养的宠物"},
                    "small": {"chinese": "小型", "description": "适合小型宠物"},
                    "puppy": {"chinese": "幼犬", "description": "适合幼犬"},
                    "kitten": {"chinese": "幼猫", "description": "适合幼猫"},
                    "medium": {"chinese": "中型", "description": "适合中型宠物"},
                    "large": {"chinese": "大型", "description": "适合大型宠物"}
                }
                
                # 定义产品类别关键词
                product_types = list(product_type_mapping.keys())
                features = list(feature_mapping.keys())
                materials = list(material_mapping.keys())
                targets = list(target_mapping.keys())
                
                # 统计函数
                def count_keywords(keywords, column, mapping):
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
                    
                    # 转换成带有中文和描述的结果
                    enriched_result = {}
                    for keyword, count in result.items():
                        if keyword in mapping:
                            enriched_result[keyword] = {
                                "count": count,
                                "chinese": mapping[keyword]["chinese"],
                                "description": mapping[keyword]["description"]
                            }
                        else:
                            enriched_result[keyword] = {
                                "count": count,
                                "chinese": "",
                                "description": ""
                            }
                    
                    # 按计数降序排序
                    return {k: v for k, v in sorted(
                        enriched_result.items(), 
                        key=lambda item: item[1]["count"], 
                        reverse=True
                    )}
                
                # 进行统计
                product_stats = count_keywords(product_types, title_column, product_type_mapping)
                feature_stats = count_keywords(features, title_column, feature_mapping)
                material_stats = count_keywords(materials, title_column, material_mapping)
                target_stats = count_keywords(targets, title_column, target_mapping)
                
                # 显示结果
                st.subheader("1. 产品类型变体关键词统计")
                product_df = pd.DataFrame({
                    "英文关键词": [k for k in product_stats.keys()],
                    "中文对应词": [v["chinese"] for v in product_stats.values()],
                    "产品描述": [v["description"] for v in product_stats.values()],
                    "评论数累计": [v["count"] for v in product_stats.values()]
                })
                st.dataframe(product_df)
                
                st.subheader("2. 功能特性关键词统计")
                feature_df = pd.DataFrame({
                    "英文关键词": [k for k in feature_stats.keys()],
                    "中文对应词": [v["chinese"] for v in feature_stats.values()],
                    "功能描述": [v["description"] for v in feature_stats.values()],
                    "评论数累计": [v["count"] for v in feature_stats.values()]
                })
                st.dataframe(feature_df)
                
                st.subheader("3. 材质特征关键词统计")
                material_df = pd.DataFrame({
                    "英文关键词": [k for k in material_stats.keys()],
                    "中文对应词": [v["chinese"] for v in material_stats.values()],
                    "材质描述": [v["description"] for v in material_stats.values()],
                    "评论数累计": [v["count"] for v in material_stats.values()]
                })
                st.dataframe(material_df)
                
                st.subheader("4. 适用对象关键词统计")
                target_df = pd.DataFrame({
                    "英文关键词": [k for k in target_stats.keys()],
                    "中文对应词": [v["chinese"] for v in target_stats.values()],
                    "适用描述": [v["description"] for v in target_stats.values()],
                    "评论数累计": [v["count"] for v in target_stats.values()]
                })
                st.dataframe(target_df)
                
                # 5. 添加高累计量关键词组合分析
                st.subheader("5. 高累计量关键词组合")
                
                # 从每类选择前两个高频关键词
                top_products = list(product_stats.keys())[:2] if product_stats else []
                top_features = list(feature_stats.keys())[:2] if feature_stats else []
                top_materials = list(material_stats.keys())[:2] if material_stats else []
                top_targets = list(target_stats.keys())[:2] if target_stats else []
                
                # 生成组合
                combinations = []
                
                if top_products and top_features:
                    combinations.append((top_products[0], top_features[0]))
                if top_products and top_materials:
                    combinations.append((top_products[0], top_materials[0]))
                if top_products and top_targets:
                    combinations.append((top_products[0], top_targets[0]))
                if top_features and top_materials:
                    combinations.append((top_features[0], top_materials[0]))
                
                # 计算组合的累计量
                combo_results = []
                for combo in combinations:
                    word1, word2 = combo
                    word1_count = next((v["count"] for k, v in product_stats.items() if k == word1), 
                                       next((v["count"] for k, v in feature_stats.items() if k == word1),
                                           next((v["count"] for k, v in material_stats.items() if k == word1),
                                               next((v["count"] for k, v in target_stats.items() if k == word1), 0))))
                    
                    word2_count = next((v["count"] for k, v in product_stats.items() if k == word2), 
                                       next((v["count"] for k, v in feature_stats.items() if k == word2),
                                           next((v["count"] for k, v in material_stats.items() if k == word2),
                                               next((v["count"] for k, v in target_stats.items() if k == word2), 0))))
                    
                    # 获取中文翻译
                    word1_chinese = ""
                    if word1 in product_type_mapping:
                        word1_chinese = product_type_mapping[word1]["chinese"]
                    elif word1 in feature_mapping:
                        word1_chinese = feature_mapping[word1]["chinese"]
                    elif word1 in material_mapping:
                        word1_chinese = material_mapping[word1]["chinese"]
                    elif word1 in target_mapping:
                        word1_chinese = target_mapping[word1]["chinese"]
                    
                    word2_chinese = ""
                    if word2 in product_type_mapping:
                        word2_chinese = product_type_mapping[word2]["chinese"]
                    elif word2 in feature_mapping:
                        word2_chinese = feature_mapping[word2]["chinese"]
                    elif word2 in material_mapping:
                        word2_chinese = material_mapping[word2]["chinese"]
                    elif word2 in target_mapping:
                        word2_chinese = target_mapping[word2]["chinese"]
                    
                    combo_results.append({
                        "英文组合关键词": f"{word1} {word2}",
                        "中文对应词": f"{word1_chinese}{word2_chinese}",
                        "评论数累计": word1_count + word2_count
                    })
                
                # 按累计量降序排序
                combo_results.sort(key=lambda x: x["评论数累计"], reverse=True)
                
                # 显示组合结果
                combo_df = pd.DataFrame(combo_results)
                st.dataframe(combo_df)
                
                st.success("分析完成!")

