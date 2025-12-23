import streamlit as st
import random
import json

# 设置页面
st.set_page_config(
    page_title="智能文案生成器",
    page_icon="✨",
    layout="wide"
)

st.title("✨ 智能文案生成器")

# ---------- 主题分类 ----------
TOPIC_CATEGORIES = {
    "美食餐饮": {
        "keywords": ["火锅", "烧烤", "咖啡", "甜品", "日料", "西餐", "快餐", "自助餐"],
        "template_type": "food"
    },
    "情感生活": {
        "keywords": ["暗恋", "失恋", "友情", "亲情", "成长", "回忆", "孤独", "幸福"],
        "template_type": "emotional"
    },
    "旅行户外": {
        "keywords": ["旅行", "露营", "登山", "海岛", "古镇", "自驾", "背包客", "摄影"],
        "template_type": "travel"
    },
    "学习成长": {
        "keywords": ["读书", "学习", "考研", "考试", "技能", "健身", "瑜伽", "冥想"],
        "template_type": "learning"
    },
    "工作职场": {
        "keywords": ["面试", "加班", "同事", "晋升", "创业", "会议", "跳槽", "办公"],
        "template_type": "work"
    },
    "娱乐休闲": {
        "keywords": ["电影", "音乐", "游戏", "运动", "购物", "聚会", "KTV", "展览"],
        "template_type": "entertainment"
    }
}

# ---------- 智能关键词库 ----------
KEYWORD_SYSTEM = {
    "火锅": {
        "recommend_keywords": ["麻辣", "鲜香", "毛肚", "鸭肠", "服务", "环境", "热闹", "过瘾", "牛油", "酥肉"],
        "dishes": ["鲜毛肚", "嫩牛肉", "手工虾滑", "黄喉", "鸭血", "脑花", "酥肉", "红糖糍粑"],
        "tastes": ["麻辣鲜香", "醇厚浓郁", "回味无穷", "香辣过瘾", "辣而不燥"],
        "environments": ["热闹温馨", "装修精致", "氛围浓厚", "干净整洁", "有特色"],
        "services": ["热情周到", "响应及时", "专业细致", "贴心服务", "态度友好"],
        "short_slogans": ["麻辣鲜香，回味无穷", "火锅界的扛把子", "一锅红油，万千滋味", "舌尖上的麻辣狂欢",
                          "冬日里的暖心选择"]
    },
    "烧烤": {
        "recommend_keywords": ["炭火", "香气", "烤串", "啤酒", "夜宵", "聚会", "氛围", "调料", "新鲜", "烟火"],
        "dishes": ["羊肉串", "烤茄子", "烤韭菜", "烤馒头", "烤玉米", "烤鸡翅", "烤生蚝"],
        "tastes": ["孜然香气", "炭火味足", "外焦里嫩", "香辣可口", "咸淡适中"],
        "environments": ["烟火气息", "热闹非凡", "简约大方", "干净卫生", "有氛围"],
        "services": ["快速高效", "热情好客", "主动推荐", "及时上菜", "服务到位"],
        "short_slogans": ["炭火香气，美味在线", "夜宵首选，烧烤狂欢", "一串入魂，满口留香", "烧烤配啤酒，快乐常有",
                          "烟火气息，人间美味"]
    },
    "暗恋": {
        "recommend_keywords": ["青涩", "心动", "偷偷", "日记", "青春", "美好", "遗憾", "成长", "纯真", "脸红"],
        "emotions": ["小鹿乱撞", "忐忑不安", "甜蜜期待", "患得患失", "心跳加速"],
        "scenes": ["教室窗边", "操场跑道", "图书馆角落", "放学路上", "食堂排队"],
        "actions": ["偷看背影", "写日记", "制造偶遇", "听ta喜欢的歌", "保存聊天记录"],
        "insights": ["青涩的美好", "成长的代价", "纯真的感情", "青春的印记", "时间的礼物"],
        "short_slogans": ["青春里最美好的秘密", "藏在心底的喜欢", "偷偷喜欢，慢慢长大", "暗恋是一场独角戏",
                          "那些没说出口的喜欢"]
    },
    "失恋": {
        "recommend_keywords": ["痛苦", "眼泪", "时间", "疗愈", "成长", "放下", "释怀", "坚强", "重生", "独立"],
        "emotions": ["心如刀割", "泪流满面", "失魂落魄", "痛苦挣扎", "慢慢释怀"],
        "stages": ["初期痛苦", "反复挣扎", "逐渐接受", "开始成长", "真正放下"],
        "methods": ["时间疗伤", "朋友陪伴", "自我提升", "转移注意", "接纳现实"],
        "gains": ["更加坚强", "更懂自己", "珍惜当下", "成长成熟", "重新出发"],
        "short_slogans": ["告别过去，迎接新生", "失恋是成长的开始", "放下是为了更好的开始", "时间是治愈的良药",
                          "失恋后，我长大了"]
    },
    "旅行": {
        "recommend_keywords": ["风景", "探索", "自由", "文化", "体验", "记忆", "冒险", "放松", "发现", "摄影"],
        "attractions": ["古镇小巷", "山川湖海", "历史遗迹", "现代都市", "自然风光"],
        "feelings": ["心灵放松", "视野开阔", "文化震撼", "自由自在", "难忘体验"],
        "experiences": ["当地美食", "特色文化", "风土人情", "独特风景", "深度探索"],
        "harvests": ["美好回忆", "成长见识", "心灵洗涤", "放松心情", "开阔眼界"],
        "short_slogans": ["在路上，遇见更好的自己", "世界那么大，我想去看看", "旅行让心灵自由飞翔", "每一次出发都是新生",
                          "风景在远方，梦想在路上"]
    },
    "读书": {
        "recommend_keywords": ["思考", "智慧", "安静", "沉浸", "启发", "知识", "心灵", "成长", "世界", "感悟"],
        "types": ["文学经典", "历史传记", "哲学思考", "心理学", "自我成长"],
        "feelings": ["心灵共鸣", "思想启迪", "知识增长", "内心平静", "视野开阔"],
        "harvests": ["思维升级", "认知提升", "情感丰富", "智慧增长", "内心强大"],
        "methods": ["深度阅读", "思考笔记", "实践应用", "分享讨论", "反复品味"],
        "short_slogans": ["书中自有黄金屋", "阅读让灵魂更丰富", "一本好书，一个世界", "在书海中寻找智慧",
                          "读书是最好的投资"]
    }
}

# ---------- 模板库 ----------
TEMPLATE_SYSTEM = {
    "food": {
        "dishes": ["招牌菜", "特色菜", "人气菜", "秘制菜", "招牌小吃", "创意菜品", "经典菜式"],
        "tastes": ["美味可口", "香气四溢", "口感丰富", "味道独特", "鲜美多汁"],
        "environments": ["环境舒适", "装修精致", "氛围温馨", "干净整洁", "设计感强"],
        "services": ["服务周到", "热情专业", "细心体贴", "快速响应", "耐心解答"],
        "short_slogans": ["美味享受，就在这里", "食在味蕾，乐在心头", "每一口都是幸福", "美食与爱不可辜负"]
    },
    "emotional": {
        "emotions": ["感动温暖", "心潮澎湃", "思绪万千", "感慨万千", "情感丰富"],
        "scenes": ["某个时刻", "某个地方", "某个瞬间", "某个场景", "某段时光"],
        "actions": ["回忆往事", "品味心情", "感悟生活", "思考人生", "体验情感"],
        "insights": ["人生的感悟", "成长的意义", "情感的价值", "时间的礼物", "生命的体验"],
        "short_slogans": ["情感的温度，记忆的厚度", "心中所感，笔下生花", "情感世界，丰富人生", "用心感受，用情表达"]
    },
    "travel": {
        "attractions": ["美丽风景", "人文景点", "自然奇观", "历史遗迹", "特色建筑"],
        "feelings": ["心旷神怡", "视野开阔", "心灵净化", "自由自在", "难忘经历"],
        "experiences": ["当地特色", "文化体验", "风土人情", "独特活动", "新鲜尝试"],
        "harvests": ["美好回忆", "成长收获", "心灵感悟", "人生体验", "开阔眼界"],
        "short_slogans": ["行在路上，心在远方", "旅行发现更好的自己", "世界的风景在眼前", "每一次旅行都是新生"]
    },
    "learning": {
        "types": ["知识学习", "技能提升", "思维训练", "专业进修", "兴趣培养"],
        "feelings": ["充实满足", "收获满满", "进步成长", "思维开阔", "信心增强"],
        "harvests": ["知识积累", "能力提升", "视野拓展", "思维升级", "自信建立"],
        "methods": ["系统学习", "实践应用", "思考总结", "交流分享", "持续进步"],
        "short_slogans": ["学习改变命运", "知识就是力量", "每一天都在进步", "学习是最好的投资"]
    },
    "work": {
        "emotions": ["充实忙碌", "挑战成长", "团队合作", "成就满足", "职业发展"],
        "stages": ["职业规划", "工作执行", "团队协作", "问题解决", "成果总结"],
        "methods": ["专业专注", "沟通协作", "创新思考", "高效执行", "持续改进"],
        "gains": ["职业成长", "经验积累", "能力提升", "团队合作", "成就获得"],
        "short_slogans": ["职场成长，成就自我", "工作让生活更精彩", "专业成就价值", "职场路上的每一步"]
    },
    "entertainment": {
        "dishes": ["娱乐项目", "休闲活动", "玩乐体验", "游戏内容", "表演节目"],
        "tastes": ["欢乐有趣", "轻松愉快", "刺激好玩", "放松享受", "精彩纷呈"],
        "environments": ["氛围活跃", "环境舒适", "设施完善", "布置精美", "灯光音响"],
        "services": ["服务贴心", "安排周到", "专业指导", "安全保障", "体验流畅"],
        "short_slogans": ["玩乐中放松心情", "娱乐让生活更美好", "快乐时光，轻松享受", "娱乐休闲，丰富生活"]
    }
}


# ---------- 词库管理器 ----------
class KeywordManager:
    def __init__(self):
        # 深拷贝默认词库
        self.keyword_system = {k: v.copy() for k, v in KEYWORD_SYSTEM.items()}
        self.current_category = None

    def set_category(self, category):
        """设置当前分类"""
        self.current_category = category

    def import_json(self, json_str):
        """导入JSON格式词库"""
        try:
            custom_data = json.loads(json_str)
            imported_count = 0

            for topic, data in custom_data.items():
                if topic in self.keyword_system:
                    # 合并到现有主题
                    for key, value in data.items():
                        if key in self.keyword_system[topic]:
                            # 如果是列表就合并
                            if isinstance(value, list):
                                self.keyword_system[topic][key] = list(set(self.keyword_system[topic][key] + value))
                            else:
                                self.keyword_system[topic][key] = value
                        else:
                            self.keyword_system[topic][key] = value
                else:
                    # 新增主题
                    self.keyword_system[topic] = data

                imported_count += 1

            return True, f"✅ 成功导入 {imported_count} 个主题！"
        except json.JSONDecodeError:
            return False, "❌ JSON格式错误！请检查格式。"
        except Exception as e:
            return False, f"❌ 导入失败：{str(e)}"

    def get_recommended_keywords(self, topic):
        """智能推荐关键词（使用当前词库）"""
        # 如果有选中的分类，优先使用分类模板
        if self.current_category and self.current_category in TOPIC_CATEGORIES:
            category_data = TOPIC_CATEGORIES[self.current_category]
            template_type = category_data["template_type"]

            if template_type == "food":
                return ["美味", "口感", "环境", "服务", "菜品", "特色", "推荐", "体验"]
            elif template_type == "emotional":
                return ["情感", "感受", "心情", "回忆", "成长", "体验", "温暖", "感悟"]
            elif template_type == "travel":
                return ["风景", "体验", "行程", "景点", "文化", "记忆", "自由", "探索"]
            elif template_type == "learning":
                return ["学习", "知识", "方法", "收获", "进步", "思考", "提升", "成长"]
            elif template_type == "work":
                return ["工作", "职场", "团队", "任务", "成果", "挑战", "发展", "经验"]
            elif template_type == "entertainment":
                return ["娱乐", "休闲", "体验", "活动", "乐趣", "放松", "享受", "节目"]

        topic_lower = topic.lower()

        # 先精确匹配
        for key in self.keyword_system.keys():
            if key in topic_lower:
                return self.keyword_system[key].get("recommend_keywords", ["体验", "感受"])

        # 智能匹配
        if any(word in topic_lower for word in ["火锅", "麻辣", "涮锅"]):
            return self.keyword_system["火锅"]["recommend_keywords"]
        elif any(word in topic_lower for word in ["烧烤", "烤串", "烤肉"]):
            return self.keyword_system["烧烤"]["recommend_keywords"]
        elif any(word in topic_lower for word in ["暗恋", "初恋", "喜欢"]):
            return self.keyword_system["暗恋"]["recommend_keywords"]
        elif any(word in topic_lower for word in ["失恋", "分手", "结束"]):
            return self.keyword_system["失恋"]["recommend_keywords"]
        elif any(word in topic_lower for word in ["旅行", "旅游", "游记"]):
            return self.keyword_system["旅行"]["recommend_keywords"]
        elif any(word in topic_lower for word in ["读书", "阅读", "书籍"]):
            return self.keyword_system["读书"]["recommend_keywords"]
        else:
            return ["体验", "感受", "成长", "思考", "收获"]

    def get_topic_data(self, topic, user_keywords=""):
        """获取主题数据"""
        # 如果有选中的分类，使用分类模板
        if self.current_category and self.current_category in TOPIC_CATEGORIES:
            category_data = TOPIC_CATEGORIES[self.current_category]
            template_type = category_data["template_type"]
            template_data = TEMPLATE_SYSTEM[template_type]

            # 根据用户关键词增强模板
            enhanced_data = self._enhance_template_with_keywords(template_data, user_keywords, template_type)

            # 根据模板类型返回相应的数据结构
            if template_type == "food" or template_type == "entertainment":
                return {
                    "dishes": enhanced_data["dishes"],
                    "tastes": enhanced_data["tastes"],
                    "environments": enhanced_data["environments"],
                    "services": enhanced_data["services"],
                    "short_slogans": enhanced_data["short_slogans"],
                    "recommend_keywords": self.get_recommended_keywords(topic)
                }
            elif template_type == "emotional" or template_type == "work":
                return {
                    "emotions": enhanced_data["emotions"],
                    "scenes": enhanced_data.get("scenes", ["某个地方"]),
                    "actions": enhanced_data.get("actions", ["经历"]),
                    "insights": enhanced_data.get("insights", ["感悟"]),
                    "stages": enhanced_data.get("stages", ["过程"]),
                    "methods": enhanced_data.get("methods", ["方法"]),
                    "gains": enhanced_data.get("gains", ["成长"]),
                    "short_slogans": enhanced_data["short_slogans"],
                    "recommend_keywords": self.get_recommended_keywords(topic)
                }
            elif template_type == "travel":
                return {
                    "attractions": enhanced_data["attractions"],
                    "feelings": enhanced_data["feelings"],
                    "experiences": enhanced_data["experiences"],
                    "harvests": enhanced_data["harvests"],
                    "short_slogans": enhanced_data["short_slogans"],
                    "recommend_keywords": self.get_recommended_keywords(topic)
                }
            elif template_type == "learning":
                return {
                    "types": enhanced_data["types"],
                    "feelings": enhanced_data["feelings"],
                    "harvests": enhanced_data["harvests"],
                    "methods": enhanced_data["methods"],
                    "short_slogans": enhanced_data["short_slogans"],
                    "recommend_keywords": self.get_recommended_keywords(topic)
                }

        topic_lower = topic.lower()

        for key in self.keyword_system.keys():
            if key in topic_lower:
                return self.keyword_system[key]

        if any(word in topic_lower for word in ["火锅", "麻辣", "涮锅"]):
            return self.keyword_system["火锅"]
        elif any(word in topic_lower for word in ["烧烤", "烤串", "烤肉"]):
            return self.keyword_system["烧烤"]
        elif any(word in topic_lower for word in ["暗恋", "初恋", "喜欢"]):
            return self.keyword_system["暗恋"]
        elif any(word in topic_lower for word in ["失恋", "分手", "结束"]):
            return self.keyword_system["失恋"]
        elif any(word in topic_lower for word in ["旅行", "旅游", "游记"]):
            return self.keyword_system["旅行"]
        elif any(word in topic_lower for word in ["读书", "阅读", "书籍"]):
            return self.keyword_system["读书"]
        else:
            # 默认使用情感类模板
            return self.keyword_system["暗恋"]

    def _enhance_template_with_keywords(self, template_data, user_keywords, template_type):
        """使用用户关键词增强模板数据"""
        if not user_keywords:
            return template_data

        user_kw_list = [k.strip() for k in user_keywords.split(',') if k.strip()]
        enhanced_data = template_data.copy()

        # 根据模板类型将用户关键词加入到相应的字段
        if template_type in ["food", "entertainment"]:
            # 将用户关键词加入到菜品/项目、口味等字段
            for kw in user_kw_list:
                if len(kw) <= 4:  # 短关键词更适合作为形容词
                    if kw not in enhanced_data["tastes"]:
                        enhanced_data["tastes"].insert(0, kw)
                    if kw not in enhanced_data["services"]:
                        enhanced_data["services"].insert(0, kw)
                else:  # 长关键词可能更适合作为项目名称
                    if kw not in enhanced_data["dishes"]:
                        enhanced_data["dishes"].insert(0, kw)

        elif template_type in ["emotional", "work", "learning", "travel"]:
            # 将用户关键词加入到情感、收获等字段
            for kw in user_kw_list:
                if "emotions" in enhanced_data and kw not in enhanced_data["emotions"]:
                    enhanced_data["emotions"].insert(0, kw)
                if "feelings" in enhanced_data and kw not in enhanced_data["feelings"]:
                    enhanced_data["feelings"].insert(0, kw)
                if "harvests" in enhanced_data and kw not in enhanced_data["harvests"]:
                    enhanced_data["harvests"].insert(0, kw)
                if "gains" in enhanced_data and kw not in enhanced_data["gains"]:
                    enhanced_data["gains"].insert(0, kw)

        return enhanced_data


# ---------- 智能内容生成 ----------
class SmartGenerator:
    def __init__(self, keyword_manager):
        self.km = keyword_manager

    def generate_content(self, topic, style, length="标准长度", user_keywords=""):
        """智能生成内容"""
        # 使用用户关键词获取增强的主题数据
        topic_data = self.km.get_topic_data(topic, user_keywords)

        # 判断是否是美食或娱乐类（使用dishes模板）
        is_food_template = "dishes" in topic_data

        # 处理关键词
        if user_keywords:
            user_kw_list = [k.strip() for k in user_keywords.split(',') if k.strip()]
            # 优先使用用户关键词
            all_keywords = user_kw_list
        else:
            all_keywords = topic_data.get("recommend_keywords", ["体验", "感受"])[:5]

        if length == "超短文案":
            # 改进的超短文案生成
            if user_keywords:
                user_kw_list = [k.strip() for k in user_keywords.split(',') if k.strip()]
                if user_kw_list:
                    # 使用用户关键词生成更个性化的短文案
                    kw = random.choice(user_kw_list)
                    short_templates = [
                        f"{topic}：{kw}的极致体验",
                        f"感受{topic}的{kw}魅力",
                        f"{kw}与{topic}的完美邂逅",
                        f"关于{topic}的{kw}记忆",
                        f"{topic}，{kw}的独到之处"
                    ]
                    return random.choice(short_templates)

            # 使用模板中的短文案
            short_slogans = topic_data.get("short_slogans", [f"{topic}，值得一试"])
            return random.choice(short_slogans)

        if style == "感性叙事":
            content = self._generate_emotional(topic, topic_data, all_keywords, is_food_template)
        elif style == "理性分析":
            content = self._generate_rational(topic, topic_data, all_keywords, is_food_template)
        elif style == "专业测评":
            content = self._generate_professional(topic, topic_data, all_keywords, is_food_template)
        elif style == "轻松活泼":
            content = self._generate_casual(topic, topic_data, all_keywords, is_food_template)
        elif style == "深度思考":
            content = self._generate_philosophical(topic, topic_data, all_keywords, is_food_template)
        else:
            content = self._generate_emotional(topic, topic_data, all_keywords, is_food_template)

        return content

    def _generate_emotional(self, topic, topic_data, keywords, is_food_template):
        # 使用用户关键词
        user_keywords = keywords[:3] if keywords else []
        keyword_str = "、".join(user_keywords) if user_keywords else "难忘"

        if is_food_template:
            # 从关键词中选取或使用模板
            dish_keyword = user_keywords[0] if user_keywords and len(user_keywords[0]) <= 4 else random.choice(
                topic_data.get("dishes", ["美食"]))
            taste_keyword = user_keywords[1] if len(user_keywords) > 1 and len(
                user_keywords[1]) <= 4 else random.choice(topic_data.get("tastes", ["美味"]))
            env = random.choice(topic_data.get("environments", ["舒适环境"]))
            service = random.choice(topic_data.get("services", ["周到服务"]))

            return f"""关于「{topic}」的记忆，总是与{keyword_str}紧密相连。

走进店里，{env}的氛围让人倍感舒适。{dish_keyword}带着{taste_keyword}的诱惑，让人食欲大开。

最难忘的是与朋友共享的欢乐时光，{service}的服务让整个体验更加完美。

那些与{keyword_str}相关的美好瞬间，如今回想起来依然温暖如初。"""
        else:
            emotion_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("emotions", ["感动"]))
            scene = random.choice(topic_data.get("scenes", ["某个地方"]))
            action = random.choice(topic_data.get("actions", ["经历"]))
            insight = random.choice(topic_data.get("insights", ["感悟"]))

            return f"""关于「{topic}」，那些与{keyword_str}相关的记忆依然鲜活。

还记得{scene}的那个午后，{action}的时候，{emotion_keyword}的感觉如潮水般涌来。

那段经历让我深刻体会到{insight}的{emotion_keyword.lower()}，成为我人生中宝贵的财富。

现在回想起来，依然会为那些真挚的{keyword_str}而深深感动。"""

    def _generate_rational(self, topic, topic_data, keywords, is_food_template):
        user_keywords = keywords[:3] if keywords else []

        if is_food_template:
            dish_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("dishes", ["特色菜"]))
            taste_keyword = user_keywords[1] if len(user_keywords) > 1 else random.choice(
                topic_data.get("tastes", ["美味"]))
            env = random.choice(topic_data.get("environments", ["舒适环境"]))
            service = random.choice(topic_data.get("services", ["良好服务"]))

            keyword_str = "、".join(user_keywords) if user_keywords else "综合"

            return f"""📊 「{topic}」分析报告

📌 关键词：{keyword_str}
环境评估：{env}
特色推荐：{dish_keyword}（{taste_keyword}）
服务水平：{service}

💡 综合评价：在{keyword_str}方面表现突出，体验良好
🎯 推荐指数：★★★★☆
👥 适合人群：注重{keyword_str}体验的各类人群"""
        else:
            emotion_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("emotions", ["情感"]))
            stage = random.choice(topic_data.get("stages", ["过程"]))
            method = random.choice(topic_data.get("methods", ["方法"]))
            gain = random.choice(topic_data.get("gains", ["成长"]))

            keyword_str = "、".join(user_keywords) if user_keywords else "情感"

            return f"""📊 「{topic}」分析报告

📌 关键词：{keyword_str}
情感特征：{emotion_keyword}
发展阶段：{stage}
应对方法：通过{method}来处理{keyword_str}
长期收获：{gain}

💡 综合建议：理性面对{keyword_str}，从中获得{keyword_str}的{getattr(topic_data, 'harvests', ['成长'])[0] if hasattr(topic_data, 'harvests') else '成长'}"""

    def _generate_professional(self, topic, topic_data, keywords, is_food_template):
        user_keywords = keywords[:3] if keywords else []

        if is_food_template:
            dish_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("dishes", ["招牌菜"]))
            taste_keyword = user_keywords[1] if len(user_keywords) > 1 else random.choice(
                topic_data.get("tastes", ["美味"]))
            service = random.choice(topic_data.get("services", ["专业服务"]))

            keyword_str = "、".join(user_keywords) if user_keywords else "品质"

            return f"""⭐️ 「{topic}」专业测评

📊 测评维度：{keyword_str}
🏠 环境体验：8.5/10（舒适度佳）
🍽️ 特色项目：{dish_keyword} 9.0/10（{taste_keyword}突出）
🎯 品质感受：{taste_keyword} 8.8/10
👨‍🍳 服务水平：{service} 8.6/10

📈 综合得分：8.7/10
💎 专业评价：在{keyword_str}方面表现优异，细节处理到位
🏆 推荐等级：A级推荐（特别适合追求{keyword_str}的消费者）"""
        else:
            emotion_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("emotions", ["情感"]))
            insight = random.choice(topic_data.get("insights", ["成长"]))

            keyword_str = "、".join(user_keywords) if user_keywords else "体验"

            return f"""⭐️ 「{topic}」专业测评

📊 测评维度：{keyword_str}深度
💖 情感深度：8.5/10（{emotion_keyword}强烈）
🌱 成长价值：9.0/10（促进{insight}）
🎭 体验丰富度：8.2/10（{keyword_str}多样）
⏳ 影响持久度：8.8/10（{keyword_str}记忆深刻）

📈 综合评分：8.6/10
💎 专业评价：具有深刻的{insight}价值，{keyword_str}层面表现突出
🏆 推荐指数：⭐⭐⭐⭐☆（适合寻求{keyword_str}深度的用户）"""

    def _generate_casual(self, topic, topic_data, keywords, is_food_template):
        user_keywords = keywords[:3] if keywords else []
        keyword_str = "、".join(user_keywords) if user_keywords else "超赞"

        if is_food_template:
            dish_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("dishes", ["美食"]))
            taste_keyword = user_keywords[1] if len(user_keywords) > 1 else random.choice(
                topic_data.get("tastes", ["美味"]))

            return f"""😄 「{topic}」真的绝了！{keyword_str}体验满分！

{taste_keyword}的感觉太棒了，{dish_keyword}简直让人欲罢不能！

人均消费合理，{keyword_str}的性价比超高！

强烈推荐给所有朋友，特别是喜欢{keyword_str}的小伙伴！

快约上朋友一起去感受{topic}的{keyword_str}魅力吧！"""
        else:
            emotion_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("emotions", ["兴奋"]))
            action = random.choice(topic_data.get("actions", ["经历"]))

            return f"""😄 关于「{topic}」我有太多话要说！{keyword_str}到不行！

那种{emotion_keyword}的感觉真的让人上头，{keyword_str}体验爆棚！

{action}的时候{keyword_str}又有趣，现在想想都忍不住笑出声！

真心推荐大家去体验一下{topic}的{keyword_str}，绝对不会让你失望！

相信我，这绝对是一次{keyword_str}到爆的难忘经历！"""

    def _generate_philosophical(self, topic, topic_data, keywords, is_food_template):
        user_keywords = keywords[:2] if keywords else []
        keyword_str = "、".join(user_keywords) if user_keywords else "深刻"

        if is_food_template:
            taste_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("tastes", ["美味"]))

            return f"""💭 「{topic}」：关于{keyword_str}体验的哲学思考

{topic}不仅是一种物质享受，更是一种关于{keyword_str}的精神探索。

在{taste_keyword}的感受中，我们寻找的不仅是感官的满足，更是对{keyword_str}意义的追问。

这种{keyword_str}体验让我们暂时忘却日常的烦恼，沉浸在当下的{keyword_str}美学中。

每一次{topic}的体验都是一次与自我的{keyword_str}对话，一次对{keyword_str}价值的深度探寻。"""
        else:
            emotion_keyword = user_keywords[0] if user_keywords else random.choice(topic_data.get("emotions", ["情感"]))
            insight = random.choice(topic_data.get("insights", ["价值"]))

            return f"""💭 「{topic}」：关于{keyword_str}存在的哲学思考

{topic}不仅是一种{keyword_str}经历，更是个体与世界的{keyword_str}对话。

在{emotion_keyword}的情感波动中，我们看到的不仅是外在的现象，更是内心对{keyword_str}的映射。

这种{keyword_str}体验让我们思考存在的{insight}，探寻生命的{keyword_str}本质。

每一次{keyword_str}的体验都是一次灵魂的觉醒，一次对{keyword_str}意义的深度追问。"""


# ---------- 初始化 ----------
keyword_manager = KeywordManager()
generator = SmartGenerator(keyword_manager)

# ---------- 侧边栏：词库上传 ----------
with st.sidebar:
    st.markdown("## 📚 词库管理")

    # 方法1：文件上传
    st.subheader("📁 上传词库文件")
    uploaded_file = st.file_uploader(
        "选择JSON文件上传",
        type=['json'],
        help="上传JSON格式的自定义词库"
    )

    if uploaded_file is not None:
        try:
            json_str = uploaded_file.getvalue().decode("utf-8")
            success, message = keyword_manager.import_json(json_str)
            if success:
                st.success(message)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"文件读取失败：{str(e)}")

    # 方法2：文本输入
    st.subheader("📝 或粘贴JSON内容")
    json_input = st.text_area(
        "直接粘贴JSON词库",
        height=150,
        placeholder='{"咖啡": {"recommend_keywords": ["浓郁", "香醇"]}}'
    )

    if st.button("导入词库", key="import_btn"):
        if json_input:
            success, message = keyword_manager.import_json(json_input)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("请输入JSON内容")

    st.markdown("---")
    st.markdown("## 📖 使用说明")
    st.markdown("""
    **🎯 主题分类功能**
    1. 先选择主题分类（如美食餐饮）
    2. 所有生成内容都会使用该分类模板
    3. 输入内容自动适配模板风格

    **🔑 智能关键词功能**
    1. 用户输入的关键词会优先使用
    2. 根据所选分类智能推荐关键词
    3. 点击"使用推荐"一键填充关键词

    **📚 词库管理**
    1. 上传JSON文件 或 粘贴JSON
    2. 可扩展现有主题
    3. 可添加全新主题

    **🎨 写作风格**
    - 5种不同风格可选
    - 智能适配主题类型
    - 用户关键词深度融入
    """)

    # JSON格式示例
    with st.expander("📋 JSON格式示例"):
        st.code("""{
  "咖啡店": {
    "recommend_keywords": ["浓郁", "香醇", "环境", "音乐"],
    "tastes": ["香醇浓郁", "口感顺滑"],
    "short_slogans": ["一杯咖啡的时光"]
  }
}""")

# ---------- 主界面 ----------

# 初始化session state
if 'category_selection' not in st.session_state:
    st.session_state.category_selection = "请选择分类"
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'recommended_keywords_input' not in st.session_state:
    st.session_state.recommended_keywords_input = ""

# 主题分类选择
st.subheader("🏷️ 主题分类")
category_selection = st.selectbox(
    "选择主题分类（选择后所有生成内容都会使用该分类模板）",
    ["请选择分类"] + list(TOPIC_CATEGORIES.keys()),
    key="category_selectbox",
    help="选择一个分类后，即使输入其他内容也会按照该分类的模板生成"
)

# 保存当前分类到keyword_manager
if category_selection != "请选择分类":
    keyword_manager.set_category(category_selection)
    category_info = TOPIC_CATEGORIES[category_selection]

    # 显示分类信息
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ 已选择：{category_selection}")
    with col2:
        template_type_mapping = {
            "food": "美食模板",
            "emotional": "情感模板",
            "travel": "旅行模板",
            "learning": "学习模板",
            "work": "职场模板",
            "entertainment": "娱乐模板"
        }
        st.info(f"📝 使用模板：{template_type_mapping[category_info['template_type']]}")

    # 显示该分类下的主题示例
    example_topics = category_info["keywords"]
    st.info(f"💡 主题示例：{', '.join(example_topics[:4])}...")
else:
    st.warning("⚠️ 请先选择一个主题分类")

st.subheader("🎯 创作主题")

# 使用session state保存用户输入的主题
user_topic = st.text_input(
    "请输入您的创作主题",
    value=st.session_state.user_topic,
    key="topic_input",
    placeholder="例如：重庆火锅探店、学生时代的暗恋、周末旅行计划",
    help="输入任意内容，系统会根据所选分类自动匹配模板"
)

# 更新session state
st.session_state.user_topic = user_topic

# 智能关键词推荐
if user_topic:
    recommended_keywords = keyword_manager.get_recommended_keywords(user_topic)
    recommended_str = "、".join(recommended_keywords[:8])

    st.subheader("🔑 关键词设置")

    col1, col2 = st.columns([3, 1])

    with col1:
        # 使用session state保存关键词输入
        user_keywords = st.text_input(
            "输入关键词（用逗号分隔）",
            value=st.session_state.recommended_keywords_input,
            key="keywords_input",
            placeholder="例如：痛苦、难受、压力、熬夜（这些关键词会优先使用）",
            help="请输入2-5个关键词，系统会优先使用您的关键词"
        )
        st.session_state.recommended_keywords_input = user_keywords

    with col2:
        if st.button("使用推荐", key="use_recommend"):
            # 只更新关键词输入框，不修改主题
            st.session_state.recommended_keywords_input = ",".join(recommended_keywords[:5])
            st.success(f"✅ 已使用推荐关键词：{', '.join(recommended_keywords[:5])}")

    st.info(f"💡 智能推荐关键词：{recommended_str}")

else:
    user_keywords = st.text_input(
        "输入关键词（用逗号分隔）",
        value=st.session_state.recommended_keywords_input,
        key="keywords_input_empty",
        placeholder="例如：体验、感受、收获、成长",
        help="请输入2-5个关键词，系统会优先使用您的关键词"
    )
    st.session_state.recommended_keywords_input = user_keywords

# 风格选择
st.subheader("🎨 写作风格")
style = st.radio(
    "选择写作风格",
    ["感性叙事", "理性分析", "专业测评", "轻松活泼", "深度思考"],
    horizontal=True
)

# 内容长度
st.subheader("📏 内容长度")
length = st.radio(
    "选择内容长度",
    ["超短文案", "短篇精简", "标准长度", "详细长文"],
    horizontal=True,
    index=1
)

# 生成按钮
if st.button("🚀 生成智能文案", type="primary", use_container_width=True):
    if not user_topic:
        st.warning("请输入创作主题")
    elif category_selection == "请选择分类":
        st.warning("请先选择一个主题分类")
    else:
        content = generator.generate_content(user_topic, style, length, user_keywords)
        word_count = len(content.replace(' ', '').replace('\n', ''))

        title_styles = {
            "感性叙事": f"❤️ {user_topic}：那些与{user_keywords.split(',')[0] if user_keywords else '难忘'}相关的记忆",
            "理性分析": f"📊 {user_topic}分析报告",
            "专业测评": f"⭐️ {user_topic}专业测评",
            "轻松活泼": f"😄 超赞！{user_topic}{user_keywords.split(',')[0] if user_keywords else '体验'}分享",
            "深度思考": f"💭 {user_topic}：关于{user_keywords.split(',')[0] if user_keywords else '体验'}与思考"
        }
        title = title_styles.get(style, f"{user_topic}体验分享")

        st.session_state.current_result = {
            "title": title,
            "content": content,
            "word_count": word_count,
            "style": style,
            "length": length,
            "keywords": user_keywords if user_keywords else "使用智能推荐",
            "category": category_selection
        }

# ---------- 显示结果 ----------
if "current_result" in st.session_state:
    result = st.session_state.current_result

    st.markdown("---")

    # 显示分类信息
    if result.get('category'):
        st.info(f"📌 当前使用模板：{result['category']}")
        if result['keywords'] and result['keywords'] != "使用智能推荐":
            st.info(f"🔑 使用关键词：{result['keywords']}")

    if result['length'] == "超短文案":
        st.markdown(f"## 🎯 超短文案")
        st.markdown(f"# {result['content']}")
    else:
        st.markdown(f"# {result['title']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 字数", f"{result['word_count']}字")
    with col2:
        st.metric("🎨 风格", result['style'])
    with col3:
        if result['keywords'] and result['keywords'] != "使用智能推荐":
            kw_display = result['keywords'].split(',')[0]
            if len(result['keywords'].split(',')) > 1:
                kw_display += " 等"
            st.metric("🔑 关键词", kw_display)
        else:
            st.metric("🔑 关键词", "智能推荐")

    st.markdown("---")

    if result['length'] != "超短文案":
        st.markdown(result['content'])

    st.markdown("---")
    st.subheader("📋 复制文案")

    full_text = f"{result['title']}\n\n{result['content']}"
    st.code(full_text, language="text")

    col_copy1, col_copy2 = st.columns(2)
    with col_copy1:
        st.download_button(
            label="📥 下载文案",
            data=full_text,
            file_name=f"{result['category']}_{result['style']}_{user_topic}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_copy2:
        if st.button("🔄 重新生成", use_container_width=True):
            del st.session_state.current_result
            st.rerun()