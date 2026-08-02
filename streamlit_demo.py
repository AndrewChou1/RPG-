#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streamlit 版《幽闇地城》介面。

這個檔案是測試用的 Streamlit 介面版本，
用來展示文字 RPG 遊戲如何在瀏覽器中執行。

執行方式：
    python -m streamlit run streamlit_demo.py
"""

import random
import time
import streamlit as st

CLASSES = {
    "1": {
        "key": "warrior", "name": "戰士", "icon": "⚔️",
        "desc": "血厚攻高，正面硬剛。",
        "hp": 60, "mp": 10, "atk": 11, "def": 6,
        "skill_name": "裂地斬", "skill_mp": 6, "skill_mult": 1.9,
        "skill_desc": "造成 190% 傷害",
        "starting_weapon": "sword",
    },
    "2": {
        "key": "mage", "name": "法師", "icon": "🔮",
        "desc": "脆皮高輸出，仰賴魔力。",
        "hp": 44, "mp": 40, "atk": 8, "def": 4,
        "skill_name": "烈焰爆破", "skill_mp": 9, "skill_mult": 2.8,
        "skill_desc": "造成 260% 傷害",
        "starting_weapon": "staff",
    },
    "3": {
        "key": "rogue", "name": "盜賊", "icon": "🗡️",
        "desc": "靈巧敏捷，擅長連擊。",
        "hp": 46, "mp": 18, "atk": 9, "def": 4,
        "skill_name": "影襲連刺", "skill_mp": 8, "skill_mult": 2.2,
        "skill_desc": "造成 220% 傷害，必定命中",
        "starting_weapon": "dagger",
    },
}

WEAPONS = {
    "sword": {"key": "sword", "name": "鐵劍", "icon": "🗡️", "required_class": "warrior", "atk_bonus": 2, "def_bonus": 1, "desc": "戰士的基礎兵器。"},
    "staff": {"key": "staff", "name": "學徒法杖", "icon": "🪄", "required_class": "mage", "atk_bonus": 2, "def_bonus": 0, "desc": "法師的啟蒙法器。"},
    "dagger": {"key": "dagger", "name": "短匕首", "icon": "🗡️", "required_class": "rogue", "atk_bonus": 1, "def_bonus": 1, "desc": "盜賊的靈巧短刃。"},
}

ACCESSORIES = {
    "crystal_ball": {"key": "crystal_ball", "name": "水晶球", "icon": "🔮", "required_class": "mage", "mp_bonus": 10, "atk_bonus": 0, "def_bonus": 0, "desc": "法師的神秘道具，讓魔力更為集中。"},
    "cloak": {"key": "cloak", "name": "披風", "icon": "🧥", "required_class": "rogue", "atk_bonus": 1, "def_bonus": 1, "desc": "盜賊的隱匿披風，讓行動更靈巧。"},
    "shield": {"key": "shield", "name": "盾", "icon": "🛡️", "required_class": "warrior", "atk_bonus": 0, "def_bonus": 2, "desc": "戰士的堅固護盾，能更好地承受打擊。"},
    "abyss_guard": {"key": "abyss_guard", "name": "深淵護印", "icon": "🛡️", "required_class": "warrior", "atk_bonus": 1, "def_bonus": 4, "desc": "深淵王殞落後留下的護印，大幅強化防禦。"},
    "abyss_focus": {"key": "abyss_focus", "name": "深淵聚焦晶", "icon": "🔮", "required_class": "mage", "mp_bonus": 8, "atk_bonus": 3, "def_bonus": 1, "desc": "吸納地城魔力的晶核，強化法術輸出。"},
    "abyss_step": {"key": "abyss_step", "name": "深淵影靴", "icon": "🥾", "required_class": "rogue", "atk_bonus": 3, "def_bonus": 2, "desc": "沾染深淵氣息的影靴，讓步伐更致命。"},
}

HATS = {
    "warrior_helm": {"key": "warrior_helm", "name": "戰痕鋼盔", "icon": "🪖", "required_class": "warrior", "atk_bonus": 1, "def_bonus": 3, "desc": "刻滿戰痕的鋼盔，讓戰士在近戰中更穩健。"},
    "mage_hat": {"key": "mage_hat", "name": "祕紋法帽", "icon": "🎩", "required_class": "mage", "mp_bonus": 6, "atk_bonus": 2, "def_bonus": 1, "desc": "縫入祕紋的法帽，能聚攏魔力與專注。"},
    "rogue_hood": {"key": "rogue_hood", "name": "夜行兜帽", "icon": "🧢", "required_class": "rogue", "atk_bonus": 2, "def_bonus": 2, "desc": "吸收光線的兜帽，讓盜賊更難被鎖定。"},
}

RINGS = {
    "ring_of_fortitude": {"key": "ring_of_fortitude", "name": "勇士之戒", "icon": "💍", "required_class": "warrior", "atk_bonus": 0, "def_bonus": 2, "desc": "強化守備，讓戰士更能扛住攻擊。"},
    "ring_of_arcana": {"key": "ring_of_arcana", "name": "秘法之戒", "icon": "💍", "required_class": "mage", "atk_bonus": 1, "def_bonus": 1, "desc": "提升魔力與法術精通。"},
    "ring_of_shadow": {"key": "ring_of_shadow", "name": "影舞之戒", "icon": "💍", "required_class": "rogue", "atk_bonus": 2, "def_bonus": 0, "desc": "加強靈巧與突襲能力。"},
    "ring_of_dawn_guard": {"key": "ring_of_dawn_guard", "name": "曙光王戒", "icon": "💍", "required_class": "warrior", "atk_bonus": 2, "def_bonus": 3, "desc": "迷霧領主的核心化作王戒，令持有者屹立不倒。"},
    "ring_of_dawn_flame": {"key": "ring_of_dawn_flame", "name": "曙光秘戒", "icon": "💍", "required_class": "mage", "atk_bonus": 4, "def_bonus": 1, "desc": "自迷霧盡頭凝成的秘戒，令法術更加熾烈。"},
    "ring_of_dawn_edge": {"key": "ring_of_dawn_edge", "name": "曙光影戒", "icon": "💍", "required_class": "rogue", "atk_bonus": 4, "def_bonus": 1, "desc": "切裂晨霧的影戒，讓襲擊更凌厲。"},
}

ENEMY_POOL = [
    {"name": "地穴鼠", "icon": "🐀", "hp": 18, "atk": 5, "def": 1, "gold": (4, 8), "xp": 8},
    {"name": "骸骨兵", "icon": "💀", "hp": 26, "atk": 7, "def": 3, "gold": (6, 12), "xp": 12},
    {"name": "毒沼蛞蝓", "icon": "🐌", "hp": 22, "atk": 6, "def": 2, "gold": (5, 10), "xp": 10},
    {"name": "暗影狼", "icon": "🐺", "hp": 30, "atk": 9, "def": 2, "gold": (8, 14), "xp": 15},
    {"name": "鏽甲石像", "icon": "🗿", "hp": 40, "atk": 8, "def": 7, "gold": (10, 18), "xp": 20},
    {"name": "墓穴法師", "icon": "🧙", "hp": 28, "atk": 11, "def": 1, "gold": (10, 16), "xp": 18},
]

BOSS = {
    "name": "深淵王 · 莫拉葛斯", "icon": "👹",
    "hp": 90, "mp": 24, "atk": 13, "def": 5, "gold": (60, 90), "xp": 80,
    "skill_name": "深淵震擊", "skill_mp": 8, "skill_mult": 1.8, "skill_rate": 0.45,
}

SHOP_ITEMS = {
    "1": {"key": "potion", "name": "治療藥水", "desc": "恢復 30 點 HP", "price": 12, "icon": "🧪", "kind": "consumable"},
    "2": {"key": "ether", "name": "魔力藥水", "desc": "恢復 20 點 MP", "price": 12, "icon": "💠", "kind": "consumable"},
    "3": {"key": "elixir", "name": "萬能藥", "desc": "完全恢復 HP / MP", "price": 35, "icon": "✨", "kind": "consumable"},
    "4": {"key": "crystal_ball", "name": "水晶球", "desc": "法師專用的神秘道具", "price": 24, "icon": "🔮", "kind": "equipment", "required_class": "mage"},
    "5": {"key": "cloak", "name": "披風", "desc": "盜賊專用的隱匿披風", "price": 22, "icon": "🧥", "kind": "equipment", "required_class": "rogue"},
    "6": {"key": "shield", "name": "盾", "desc": "戰士專用的堅固護盾", "price": 26, "icon": "🛡️", "kind": "equipment", "required_class": "warrior", "slot": "accessory"},
    "7": {"key": "ring_of_fortitude", "name": "勇士之戒", "desc": "強化守備，讓戰士更能扛住攻擊。", "price": 28, "icon": "💍", "kind": "equipment", "required_class": "warrior", "slot": "ring"},
    "8": {"key": "ring_of_arcana", "name": "秘法之戒", "desc": "提升魔力與法術精通。", "price": 28, "icon": "💍", "kind": "equipment", "required_class": "mage", "slot": "ring"},
    "9": {"key": "ring_of_shadow", "name": "影舞之戒", "desc": "加強靈巧與突襲能力。", "price": 28, "icon": "💍", "kind": "equipment", "required_class": "rogue", "slot": "ring"},
}

WEAPON_UPGRADE_MAX_LEVEL = 3
WEAPON_UPGRADE_ATK_PER_LEVEL = 2
WEAPON_UPGRADE_COSTS = {
    1: 20,
    2: 35,
    3: 55,
}

SHOP_ACTION_LOCK_SECONDS = 0.8

TOTAL_FLOORS = 6

SECOND_CHAPTER_ENEMIES = [
    {"name": "迷霧狂獸", "icon": "🐗", "hp": 42, "atk": 12, "def": 4, "gold": (15, 20), "xp": 20},
    {"name": "記憶妖精", "icon": "🧚", "hp": 36, "atk": 10, "def": 4, "gold": (15, 22), "xp": 20},
    {"name": "霧影弓手", "icon": "🏹", "hp": 48, "atk": 15, "def": 6, "gold": (18, 25), "xp": 25},
    {"name": "沉睡巨岩", "icon": "🪨", "hp": 65, "atk": 14, "def": 11, "gold": (20, 28), "xp": 30},
    {"name": "幽魂術士", "icon": "👻", "hp": 46, "atk": 17, "def": 5, "gold": (22, 30), "xp": 32},
    {"name": "破曉獵人", "icon": "🦅", "hp": 53, "atk": 16, "def": 7, "gold": (24, 32), "xp": 34},
]

SECOND_CHAPTER_BOSS = {
    "name": "迷霧領主 · 塞勒斯", "icon": "🌫️",
    "hp": 175, "mp": 36, "atk": 22, "def": 10, "gold": (100, 140), "xp": 150,
    "skill_name": "迷霧崩解", "skill_mp": 10, "skill_mult": 1.9, "skill_rate": 0.5,
}

THIRD_CHAPTER_ENEMIES = [
    {"name": "幽冥魍魎", "icon": "👹", "hp": 54, "atk": 17, "def": 6, "gold": (24, 34), "xp": 30},
    {"name": "獄焰守衛", "icon": "🔥", "hp": 62, "atk": 20, "def": 8, "gold": (26, 36), "xp": 35},
    {"name": "黑暗刺客", "icon": "🗡️", "hp": 54, "atk": 21, "def": 7, "gold": (26, 38), "xp": 38},
    {"name": "破碎巨像", "icon": "🪨", "hp": 75, "atk": 19, "def": 13, "gold": (30, 44), "xp": 42},
    {"name": "深淵魔鱗", "icon": "🐉", "hp": 70, "atk": 22, "def": 9, "gold": (32, 48), "xp": 45},
    {"name": "幻影術師", "icon": "🧙‍♂️", "hp": 65, "atk": 24, "def": 7, "gold": (34, 50), "xp": 48},
]

THIRD_CHAPTER_BOSS = {
    "name": "幽冥領主 · 阿斯拉", "icon": "👑",
    "hp": 230, "mp": 45, "atk": 27, "def": 13, "gold": (130, 180), "xp": 210,
    "skill_name": "幽冥滅燼", "skill_mp": 12, "skill_mult": 2.0, "skill_rate": 0.55,
}

CHAPTER_TITLES = {
    1: "第一章：幽闇地城",
    2: "第二章：深淵之外",
    3: "第三章：幽冥之巔",
}

CHAPTER_BOSS_REWARDS = {
    1: {
        "warrior": {"slot": "hat", "key": "warrior_helm"},
        "mage": {"slot": "hat", "key": "mage_hat"},
        "rogue": {"slot": "hat", "key": "rogue_hood"},
    },
    2: {
        "warrior": {"slot": "ring", "key": "ring_of_dawn_guard"},
        "mage": {"slot": "ring", "key": "ring_of_dawn_flame"},
        "rogue": {"slot": "ring", "key": "ring_of_dawn_edge"},
    },
}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def render_red_hp_bar(current, maximum, label):
    ratio = clamp(current / maximum if maximum > 0 else 0, 0.0, 1.0)
    percent = int(round(ratio * 100))
    st.markdown(
        f"""
        <div style="margin: 0.2rem 0 0.7rem 0;">
            <div style="font-size: 0.9rem; margin-bottom: 0.25rem; color: #111;">{label}</div>
            <div style="width: 100%; background: #f3d1d1; border-radius: 999px; height: 0.9rem; overflow: hidden; border: 1px solid #d79a9a;">
                <div style="width: {percent}%; background: linear-gradient(90deg, #c62828 0%, #e53935 100%); height: 100%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_blue_mp_bar(current, maximum, label):
    ratio = clamp(current / maximum if maximum > 0 else 0, 0.0, 1.0)
    percent = int(round(ratio * 100))
    st.markdown(
        f"""
        <div style="margin: 0.2rem 0 0.7rem 0;">
            <div style="font-size: 0.9rem; margin-bottom: 0.25rem; color: #111;">{label}</div>
            <div style="width: 100%; background: #d1d9f3; border-radius: 999px; height: 0.9rem; overflow: hidden; border: 1px solid #9aaad7;">
                <div style="width: {percent}%; background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%); height: 100%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


class Hero:
    def __init__(self, cls_data):
        self.class_key = cls_data["key"]
        self.class_name = cls_data["name"]
        self.name = cls_data["name"]
        self.icon = cls_data["icon"]
        self.level = 1
        self.xp = 0
        self.xp_next = self._xp_to_next()
        self.hp_max = cls_data["hp"]
        self.hp = self.hp_max
        self.mp_max = cls_data["mp"]
        self.mp = self.mp_max
        self.base_atk = cls_data["atk"]
        self.base_defense = cls_data["def"]
        self.atk = self.base_atk
        self.defense = self.base_defense
        self.skill_name = cls_data["skill_name"]
        self.skill_mp = cls_data["skill_mp"]
        self.skill_mult = cls_data["skill_mult"]
        self.gold = 20
        self.inventory = {"potion": 1, "ether": 1, "elixir": 0}
        self.equipment = {"weapon": None, "hat": None, "accessory": None, "rings": []}
        self.weapon_upgrade_level = 0
        self.equip_weapon(cls_data.get("starting_weapon"))

    def _xp_to_next(self):
        return 20 + (self.level - 1) * 18

    def is_alive(self):
        return self.hp > 0

    def status_bar(self):
        weapon = self.equipment.get("weapon")
        hat = self.equipment.get("hat")
        accessory = self.equipment.get("accessory")
        rings = self.equipment.get("rings", [])
        weapon_text = f"{weapon['icon']} {weapon['name']}" if weapon else "未裝備"
        hat_text = f"{hat['icon']} {hat['name']}" if hat else "未裝備"
        accessory_text = f"{accessory['icon']} {accessory['name']}" if accessory else "未裝備"
        ring_text = ", ".join(f"{ring['icon']} {ring['name']}" for ring in rings) if rings else "未裝備"
        return (f"{self.icon} {self.name}  Lv.{self.level}   HP {self.hp}/{self.hp_max}   "
                f"MP {self.mp}/{self.mp_max}   💰{self.gold}   "
            f"裝備:武器[{weapon_text}] 帽子[{hat_text}] 配件[{accessory_text}] 戒指[{ring_text}]")

    def equip_weapon(self, weapon_key):
        if not weapon_key:
            return False
        weapon = WEAPONS.get(weapon_key)
        if not weapon or weapon.get("required_class") != self.class_key:
            return False
        previous = self.equipment.get("weapon")
        if previous:
            self.atk -= previous.get("atk_bonus", 0)
            self.defense -= previous.get("def_bonus", 0)
        self.equipment["weapon"] = weapon
        self.atk += weapon.get("atk_bonus", 0)
        self.defense += weapon.get("def_bonus", 0)
        return True

    def equip_equipment(self, equipment_key):
        if not equipment_key:
            return False
        equipment = ACCESSORIES.get(equipment_key)
        if not equipment or equipment.get("required_class") != self.class_key:
            return False
        previous = self.equipment.get("accessory")
        if previous and previous.get("key") == equipment_key:
            return True
        new_mp_bonus = equipment.get("mp_bonus", 0)
        if previous:
            self.atk -= previous.get("atk_bonus", 0)
            self.defense -= previous.get("def_bonus", 0)
            self.mp_max -= previous.get("mp_bonus", 0)
            self.mp = min(self.mp, self.mp_max)
        self.equipment["accessory"] = equipment
        self.atk += equipment.get("atk_bonus", 0)
        self.defense += equipment.get("def_bonus", 0)
        self.mp_max += new_mp_bonus
        self.mp = min(self.mp + new_mp_bonus, self.mp_max)
        return True

    def equip_hat(self, hat_key):
        if not hat_key:
            return False
        hat = HATS.get(hat_key)
        if not hat or hat.get("required_class") != self.class_key:
            return False
        previous = self.equipment.get("hat")
        if previous and previous.get("key") == hat_key:
            return True
        new_mp_bonus = hat.get("mp_bonus", 0)
        if previous:
            self.atk -= previous.get("atk_bonus", 0)
            self.defense -= previous.get("def_bonus", 0)
            self.mp_max -= previous.get("mp_bonus", 0)
            self.mp = min(self.mp, self.mp_max)
        self.equipment["hat"] = hat
        self.atk += hat.get("atk_bonus", 0)
        self.defense += hat.get("def_bonus", 0)
        self.mp_max += new_mp_bonus
        self.mp = min(self.mp + new_mp_bonus, self.mp_max)
        return True

    def equip_ring(self, ring_key):
        if not ring_key:
            return False
        ring = RINGS.get(ring_key)
        if not ring or ring.get("required_class") != self.class_key:
            return False
        self.equipment["rings"].append(ring)
        self.atk += ring.get("atk_bonus", 0)
        self.defense += ring.get("def_bonus", 0)
        return True

    def gain_rewards(self, gold, xp):
        self.gold += gold
        self.xp += xp
        leveled = False
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.hp_max += 8
            self.mp_max += 4
            self.atk += 2
            self.defense += 1
            self.hp = self.hp_max
            self.mp = self.mp_max
            self.xp_next = self._xp_to_next()
            leveled = True
        return leveled

    def weapon_upgrade_bonus(self):
        level = getattr(self, "weapon_upgrade_level", 0)
        return level * WEAPON_UPGRADE_ATK_PER_LEVEL

    def can_upgrade_weapon(self):
        return self.equipment.get("weapon") is not None and getattr(self, "weapon_upgrade_level", 0) < WEAPON_UPGRADE_MAX_LEVEL

    def weapon_upgrade_cost(self):
        next_level = getattr(self, "weapon_upgrade_level", 0) + 1
        return WEAPON_UPGRADE_COSTS.get(next_level)

    def upgrade_weapon(self):
        if not self.equipment.get("weapon"):
            return False, "你尚未裝備武器，無法強化。"
        current_level = getattr(self, "weapon_upgrade_level", 0)
        if current_level >= WEAPON_UPGRADE_MAX_LEVEL:
            return False, "武器已達最高強化等級。"
        cost = WEAPON_UPGRADE_COSTS.get(current_level + 1)
        if cost is None:
            return False, "目前無法強化武器。"
        if self.gold < cost:
            return False, "金幣不足，無法強化武器。"

        self.gold -= cost
        self.weapon_upgrade_level = current_level + 1
        self.atk += WEAPON_UPGRADE_ATK_PER_LEVEL
        weapon_name = self.equipment["weapon"]["name"]
        return True, f"你的 {weapon_name} 強化至 +{self.weapon_upgrade_level}！"

    def use_item(self, key):
        if self.inventory.get(key, 0) <= 0:
            return False, "道具數量不足。"
        self.inventory[key] -= 1
        if key == "potion":
            self.hp = clamp(self.hp + 30, 0, self.hp_max)
            return True, "你喝下治療藥水，恢復了 30 點 HP。"
        if key == "ether":
            self.mp = clamp(self.mp + 20, 0, self.mp_max)
            return True, "你喝下魔力藥水，恢復了 20 點 MP。"
        self.hp, self.mp = self.hp_max, self.mp_max
        return True, "萬能藥的光輝籠罩全身，HP / MP 完全恢復！"

    def maybe_gain_weapon(self):
        if random.random() >= 0.2:
            return None
        weapon_key = next((key for key, weapon in WEAPONS.items() if weapon["required_class"] == self.class_key), None)
        if not weapon_key:
            return None
        if self.equipment.get("weapon") and self.equipment["weapon"]["key"] == weapon_key:
            return None
        self.equip_weapon(weapon_key)
        weapon = WEAPONS[weapon_key]
        return f"戰利品中出現了 {weapon['icon']} {weapon['name']}，你將它裝備上了。"


class Enemy:
    def __init__(self, data, floor=0, is_boss=False):
        mult = 1 + floor * 0.22 if not is_boss else 1
        self.name = data["name"]
        self.icon = data["icon"]
        self.hp_max = round(data["hp"] * mult)
        self.hp = self.hp_max
        self.mp_max = data.get("mp", 0)
        self.mp = self.mp_max
        self.atk = round(data["atk"] * mult)
        self.defense = data["def"] + (floor // 2 if not is_boss else 0)
        self.gold_range = (round(data["gold"][0] * mult), round(data["gold"][1] * mult))
        self.xp = round(data["xp"] * mult)
        self.skill_name = data.get("skill_name")
        self.skill_mp = data.get("skill_mp", 0)
        self.skill_mult = data.get("skill_mult", 1.0)
        self.skill_rate = data.get("skill_rate", 0.0)
        self.is_boss = is_boss

    def is_alive(self):
        return self.hp > 0

    def can_cast_skill(self):
        return bool(self.skill_name) and self.mp >= self.skill_mp and random.random() < self.skill_rate


def init_game_state():
    return {
        "phase": "start",
        "hero": None,
        "enemy": None,
        "chapter": 1,
        "floor": 0,
        "battle_turn": "player",
        "messages": [],
    }


def current_chapter_title(game):
    chapter = game.get("chapter", 1)
    return CHAPTER_TITLES.get(chapter, "未知章節")


def current_enemy_pool(game):
    chapter = game.get("chapter", 1)
    if chapter == 1:
        return ENEMY_POOL
    if chapter == 2:
        return SECOND_CHAPTER_ENEMIES
    return THIRD_CHAPTER_ENEMIES


def current_boss_data(game):
    chapter = game.get("chapter", 1)
    if chapter == 1:
        return BOSS
    if chapter == 2:
        return SECOND_CHAPTER_BOSS
    return THIRD_CHAPTER_BOSS


def ensure_game_state():
    if "game" not in st.session_state:
        st.session_state.game = init_game_state()
    game = st.session_state.get("game")
    hero = game.get("hero") if game else None
    if hero:
        # Backward compatibility: old saves may not have a hat slot yet.
        hero.equipment.setdefault("hat", None)
        hero.equipment.setdefault("accessory", None)
        hero.equipment.setdefault("rings", [])
        legacy_accessory = hero.equipment.get("accessory")
        if hero.equipment.get("hat") is None and legacy_accessory and legacy_accessory.get("key") in HATS:
            hero.equipment["hat"] = HATS[legacy_accessory["key"]]
            hero.equipment["accessory"] = None


def save_game(game=None):
    if game is None:
        game = st.session_state.get("game")
    if game is not None:
        st.session_state.game = game
    return game


def log(message, game=None):
    if game is None:
        game = st.session_state.get("game")
    if game is None:
        return
    game["messages"].append(message)
    save_game(game)


def create_hero(class_key, player_name):
    hero = Hero(CLASSES[class_key])
    hero.name = player_name or hero.name
    return hero


def normalize_ring(ring):
    # Normalize legacy ring entries that may miss bonus fields.
    ring_key = ring.get("key")
    ring_data = RINGS.get(ring_key)
    if ring_data is None:
        ring_data = next((r for r in RINGS.values() if r.get("name") == ring.get("name")), None)
    if ring_data is None:
        ring_data = ring
    return {
        "key": ring_data.get("key", ring.get("key")),
        "icon": ring_data.get("icon", ring.get("icon", "💍")),
        "name": ring_data.get("name", ring.get("name", "未知戒指")),
        "atk_bonus": ring_data.get("atk_bonus", ring.get("atk_bonus", 0)),
        "def_bonus": ring_data.get("def_bonus", ring.get("def_bonus", 0)),
        "desc": ring_data.get("desc", ring.get("desc", "")),
    }


def grant_boss_reward(hero, chapter):
    reward = CHAPTER_BOSS_REWARDS.get(chapter, {}).get(hero.class_key)
    if not reward:
        return None

    if reward["slot"] == "accessory":
        if not hero.equip_equipment(reward["key"]):
            return None
        item = ACCESSORIES[reward["key"]]
    elif reward["slot"] == "hat":
        if not hero.equip_hat(reward["key"]):
            return None
        item = HATS[reward["key"]]
    else:
        if not hero.equip_ring(reward["key"]):
            return None
        item = RINGS[reward["key"]]

    return f"首領的力量凝成獎勵：{item['icon']} {item['name']} 已自動裝備。"


def log_selected_class_if_needed():
    game = st.session_state.get("game")
    if not game or game.get("phase") != "start":
        return
    class_key = st.session_state.get("selected_class", "1")
    cls_data = CLASSES.get(class_key)
    if not cls_data:
        return
    last_logged = st.session_state.get("_last_logged_selected_class")
    if last_logged == class_key:
        return
    st.session_state["_last_logged_selected_class"] = class_key
    log(f"你選擇了職業：{cls_data['icon']} {cls_data['name']}（{cls_data['desc']}）", game=game)


def start_new_game():
    game = st.session_state.game
    player_name = st.session_state.get("player_name", "冒險者").strip() or "冒險者"
    game.update({
        "phase": "explore",
        "hero": create_hero(st.session_state.get("selected_class", "1"), player_name),
        "enemy": None,
        "chapter": 1,
        "floor": 0,
        "battle_turn": "player",
        "messages": [f"{player_name} 推開地城厚重的石門，冷風夾雜著霉味撲面而來。"],
    })
    save_game(game)


def start_boss_fight(game=None):
    if game is None:
        game = st.session_state.game
    boss_data = current_boss_data(game)
    game["enemy"] = Enemy(boss_data, floor=game["floor"], is_boss=True)
    game["phase"] = "battle"
    game["battle_turn"] = "player"
    save_game(game)
    chapter = game.get("chapter", 1)
    if chapter == 1:
        log("👑 深淵王甦醒，注視著你……")
    elif chapter == 2:
        log("🌫️ 霧中巨影現身，迷霧領主向你發出冷笑……")
    else:
        log("👑 幽冥王座震顫，幽冥領主現身，黑焰席捲四方……")


def advance_floor(game=None):
    if game is None:
        game = st.session_state.game
    game["floor"] += 1
    if game["floor"] >= TOTAL_FLOORS - 1:
        start_boss_fight(game)
        return
    game["phase"] = "explore"
    save_game(game)
    log(f"你來到第 {game['floor'] + 1} 層。")


def start_chapter_two(game=None):
    if game is None:
        game = st.session_state.game
    game["chapter"] = 2
    game["floor"] = 0
    game["phase"] = "explore"
    game["enemy"] = None
    log("第二章開啟：迷霧之外的荒野，未知的試煉正等待著你。", game=game)
    save_game(game)


def start_chapter_three(game=None):
    if game is None:
        game = st.session_state.game
    game["chapter"] = 3
    game["floor"] = 0
    game["phase"] = "explore"
    game["enemy"] = None
    log("第三章來臨：幽冥之巔層層考驗，勇者踏上最終挑戰。", game=game)
    save_game(game)


def handle_explore(action):
    game = st.session_state.game
    hero = game["hero"]
    if action == "continue":
        if game.get("enemy"):
            game["phase"] = "battle"
            game["battle_turn"] = "player"
            save_game(game)
            if hasattr(st, "rerun"):
                st.rerun()
            return
        if game["floor"] == TOTAL_FLOORS - 1:
            start_boss_fight(game)
            return
        roll = random.random()
        if roll < 0.75:
            pool = current_enemy_pool(game)
            base = random.choice(pool[: min(len(pool), game["floor"] + 2)])
            game["enemy"] = Enemy(base, floor=game["floor"])
            log(f"{game['enemy'].icon} {game['enemy'].name} 擋住了去路！")
            save_game(game)
            return
        elif roll < 0.95:
            gold = random.randint(8, 20) + game["floor"] * 3
            hero.gold += gold
            log(f"你發現寶箱，獲得 💰{gold} 金幣。")
            advance_floor(game)
            return
        else:
            heal = round(hero.hp_max * 0.4)
            hero.hp = clamp(hero.hp + heal, 0, hero.hp_max)
            log(f"一處清泉出現在眼前，你恢復了 {heal} 點 HP。")
            advance_floor(game)
            return
    elif action == "shop":
        game["phase"] = "shop"
        st.session_state["shop_section"] = "menu"
        log("流浪商人出現在陰影裡，向你揮了揮手。")
        save_game(game)
        if hasattr(st, "rerun"):
            st.rerun()
        return
    elif action == "rest":
        if hero.gold < 10:
            log("身上金幣不足，商人搖了搖頭，將你請出帳篷。")
        else:
            hero.gold -= 10
            hero.hp, hero.mp = hero.hp_max, hero.mp_max
            log("你在篝火旁躺下，傷口與魔力都恢復了。")
    elif action == "inventory":
        game["phase"] = "inventory"
        log("你檢視了自己的背包。")
    save_game(game)


def resolve_battle_action(game, action, item_key=None):
    hero = game["hero"]
    enemy = game["enemy"]
    if not hero or not enemy:
        return game

    if action == "attack":
        damage = max(1, hero.atk + random.randint(-2, 3) - enemy.defense)
        enemy.hp = clamp(enemy.hp - damage, 0, enemy.hp_max)
        log(f"你揮出攻擊，對 {enemy.name} 造成 {damage} 點傷害。", game=game)
    elif action == "skill":
        if hero.mp < hero.skill_mp:
            log("魔力不足，無法施展技能。", game=game)
            save_game(game)
            return game
        hero.mp -= hero.skill_mp
        damage = max(1, round(hero.atk * hero.skill_mult) + random.randint(-1, 4) - round(enemy.defense * 0.6))
        enemy.hp = clamp(enemy.hp - damage, 0, enemy.hp_max)
        log(f"你施展【{hero.skill_name}】！造成 {damage} 點傷害。", game=game)
    elif action == "item" and item_key:
        used, message = hero.use_item(item_key)
        log(message, game=game)
        if not used:
            save_game(game)
            return game
    elif action == "run":
        if random.random() < 0.55:
            log("你成功逃離了戰鬥。", game=game)
            game["phase"] = "explore"
            game["enemy"] = None
            game["battle_turn"] = "player"
            save_game(game)
            return game
        log("逃跑失敗！", game=game)

    if not enemy.is_alive():
        gold = random.randint(*enemy.gold_range)
        hero.gain_rewards(gold, enemy.xp)
        log(f"你擊敗了 {enemy.name}，獲得 💰{gold} 金幣與 {enemy.xp} 經驗值。", game=game)
        if not enemy.is_boss:
            weapon_message = hero.maybe_gain_weapon()
            if weapon_message:
                log(weapon_message, game=game)
        game["enemy"] = None
        if enemy.is_boss:
            chapter = game.get("chapter", 1)
            reward_message = grant_boss_reward(hero, chapter)
            if reward_message:
                log(reward_message, game=game)
            if chapter < 3:
                game["phase"] = "chapter_complete"
                if chapter == 1:
                    log("第一章完成！幽闇的詛咒被解開，但命運的迷霧仍在前方。", game=game)
                else:
                    log("第二章完成！迷霧中的威脅一度平息，但幽冥之巔仍然等待著你。", game=game)
            else:
                game["phase"] = "victory"
                log("幽冥領主轟然倒地，深淵之巔終於重現光明。", game=game)
        else:
            game["phase"] = "explore"
            advance_floor(game)
            return game
        game["battle_turn"] = "player"
        save_game(game)
        return game

    if enemy.is_alive() and action != "run":
        game["battle_turn"] = "enemy"
        save_game(game)
        return game

    if not hero.is_alive():
        game["phase"] = "gameover"
        game["battle_turn"] = "player"
        log("你倒下了……", game=game)
    save_game(game)
    return game


def resolve_enemy_turn(game):
    hero = game["hero"]
    enemy = game["enemy"]
    if not hero or not enemy or not enemy.is_alive():
        game["battle_turn"] = "player"
        save_game(game)
        return game

    if enemy.can_cast_skill():
        enemy.mp = clamp(enemy.mp - enemy.skill_mp, 0, enemy.mp_max)
        damage = max(
            1,
            round(enemy.atk * enemy.skill_mult) + random.randint(-1, 4) - round(hero.defense * 0.55),
        )
        hero.hp = clamp(hero.hp - damage, 0, hero.hp_max)
        log(f"{enemy.name} 施展【{enemy.skill_name}】，你受到 {damage} 點傷害！", game=game)
    else:
        damage = max(1, enemy.atk + random.randint(-2, 3) - hero.defense)
        hero.hp = clamp(hero.hp - damage, 0, hero.hp_max)
        log(f"{enemy.name} 反擊，你受到 {damage} 點傷害。", game=game)

    game["battle_turn"] = "player"
    if not hero.is_alive():
        game["phase"] = "gameover"
        log("你倒下了……", game=game)
    save_game(game)
    return game


def handle_battle(action, item_key=None):
    game = st.session_state.game
    resolve_battle_action(game, action, item_key)
    if hasattr(st, "rerun"):
        st.rerun()


def should_process_purchase(item_key, session_state=None, now=None):
    if session_state is None:
        session_state = st.session_state
    if now is None:
        now = time.monotonic()

    locked_until = session_state.get("_shop_action_locked_until", 0.0)
    if now < locked_until:
        return False

    last_time = session_state.get("_purchase_last_time", 0.0)
    last_key = session_state.get("_purchase_last_key")
    if last_key == item_key and now - last_time < 0.8:
        return False

    session_state["_purchase_last_time"] = now
    session_state["_purchase_last_key"] = item_key
    session_state["_shop_action_locked_until"] = now + SHOP_ACTION_LOCK_SECONDS
    return True


def is_shop_action_locked(session_state=None, now=None):
    if session_state is None:
        session_state = st.session_state
    if now is None:
        now = time.monotonic()
    return now < session_state.get("_shop_action_locked_until", 0.0)


def buy_item(item_key):
    game = st.session_state.game
    hero = game["hero"]
    item = SHOP_ITEMS[item_key]
    if hero.gold < item["price"]:
        log("金幣不足，無法購買。")
        return
    if item.get("kind") == "equipment":
        if item.get("required_class") != hero.class_key:
            log("這件裝備不適合你目前的職業。")
            return
        if item.get("slot") == "ring":
            if not hero.equip_ring(item["key"]):
                log("這件裝備不適合你目前的職業。")
                return
        else:
            already_owned = bool(
                hero.equipment.get("accessory")
                and hero.equipment["accessory"]["key"] == item["key"]
            )
            if already_owned:
                log("你已經擁有這個配件，無法重複購買。")
                return
            if not hero.equip_equipment(item["key"]):
                log("這件裝備不適合你目前的職業。")
                return
        hero.gold -= item["price"]
        log(f"你購買並裝備了 {item['icon']} {item['name']}。")
        save_game(game)
        if hasattr(st, "rerun"):
            st.rerun()
        return
    hero.gold -= item["price"]
    hero.inventory[item["key"]] += 1
    log(f"你購買了 {item['icon']} {item['name']}。")
    save_game(game)
    if hasattr(st, "rerun"):
        st.rerun()


def upgrade_weapon_in_shop():
    game = st.session_state.game
    hero = game["hero"]
    upgraded, message = hero.upgrade_weapon()
    log(message)
    if upgraded:
        save_game(game)
        if hasattr(st, "rerun"):
            st.rerun()


def render_left_panel():
    st.markdown("### 🎮 遊戲設定")
    st.caption("選擇職業後，點擊開始新冒險。")
    st.session_state.selected_class = st.selectbox(
        "職業",
        options=list(CLASSES.keys()),
        format_func=lambda key: f"{CLASSES[key]['icon']} {CLASSES[key]['name']}",
    )
    log_selected_class_if_needed()
    st.session_state.player_name = st.text_input("角色名稱", value=st.session_state.get("player_name", "冒險者"))
    if st.button("開始新冒險", key="start_new_game", use_container_width=True):
        start_new_game()
    if st.button("重新整理介面", key="refresh_layout", use_container_width=True):
        st.rerun()

    game = st.session_state.get("game")
    hero = game["hero"] if game else None
    if hero:
        st.markdown("---")
        st.subheader("裝備")
        weapon = hero.equipment.get("weapon")
        hat = hero.equipment.get("hat")
        accessory = hero.equipment.get("accessory")
        rings = hero.equipment.get("rings", [])
        if weapon:
            weapon_level = getattr(hero, "weapon_upgrade_level", 0)
            weapon_tag = f"+{clamp(weapon_level, 0, WEAPON_UPGRADE_MAX_LEVEL)}"
            weapon_upgrade_bonus = hero.weapon_upgrade_bonus()
            weapon_detail = f"（強化 +{weapon_upgrade_bonus} ATK）"
            st.markdown(
                f"<span style='color:#000000;'>武器：{weapon['icon']} {weapon['name']} {weapon_tag} {weapon_detail}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("武器：尚未裝備")
        if hat:
            bonus_text = []
            if hat.get("mp_bonus", 0):
                bonus_text.append(f"+{hat['mp_bonus']} MP")
            if hat.get("atk_bonus", 0):
                bonus_text.append(f"+{hat['atk_bonus']} ATK")
            if hat.get("def_bonus", 0):
                bonus_text.append(f"+{hat['def_bonus']} DEF")
            st.markdown(
                f"<span style='color:#000000;'>帽子：{hat['icon']} {hat['name']} {' '.join(bonus_text)}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("帽子：尚未裝備")
        if accessory:
            bonus_text = []
            if accessory.get("mp_bonus", 0):
                bonus_text.append(f"+{accessory['mp_bonus']} MP")
            if accessory.get("atk_bonus", 0):
                bonus_text.append(f"+{accessory['atk_bonus']} ATK")
            if accessory.get("def_bonus", 0):
                bonus_text.append(f"+{accessory['def_bonus']} DEF")
            st.markdown(
                f"<span style='color:#000000;'>配件：{accessory['icon']} {accessory['name']} {' '.join(bonus_text)}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("配件：尚未裝備")
        if rings:
            ring_groups = {}
            for ring in rings:
                ring_data = normalize_ring(ring)
                atk_bonus = ring_data["atk_bonus"]
                def_bonus = ring_data["def_bonus"]
                group_key = ring_data.get("key") or ring_data.get("name")
                if group_key not in ring_groups:
                    ring_groups[group_key] = {
                        "icon": ring_data.get("icon", "💍"),
                        "name": ring_data.get("name", "未知戒指"),
                        "desc": ring_data.get("desc", ""),
                        "count": 0,
                        "atk_total": 0,
                        "def_total": 0,
                    }
                ring_groups[group_key]["count"] += 1
                ring_groups[group_key]["atk_total"] += atk_bonus
                ring_groups[group_key]["def_total"] += def_bonus

            ring_labels = []
            for group in ring_groups.values():
                ring_labels.append(
                    f"{group['icon']} {group['name']}*{group['count']} "
                    f"[+{group['atk_total']} ATK] [+{group['def_total']} DEF]　{group['desc']}"
                )
            st.markdown("戒指：<br>" + "<br>".join(ring_labels), unsafe_allow_html=True)
        else:
            st.caption("戒指：尚未裝備")

        weapon_bonus = weapon["atk_bonus"] if weapon else 0
        weapon_upgrade_bonus = hero.weapon_upgrade_bonus() if weapon else 0
        hat_bonus = hat["atk_bonus"] if hat else 0
        accessory_bonus = accessory["atk_bonus"] if accessory else 0
        normalized_rings = [normalize_ring(ring) for ring in rings]
        ring_atk_bonus = sum(ring["atk_bonus"] for ring in normalized_rings)
        weapon_def_bonus = weapon["def_bonus"] if weapon else 0
        hat_def_bonus = hat["def_bonus"] if hat else 0
        accessory_def_bonus = accessory["def_bonus"] if accessory else 0
        ring_def_bonus = sum(ring["def_bonus"] for ring in normalized_rings)
        ring_count = len(normalized_rings)
        level_atk_bonus = (hero.level - 1) * 2
        level_def_bonus = hero.level - 1

        st.markdown(
            f"**攻擊力**：原始 {hero.base_atk} + 升級 {level_atk_bonus} + 武器 {weapon_bonus} + 強化 {weapon_upgrade_bonus} + 帽子 {hat_bonus} + 配件 {accessory_bonus} + 戒指 {ring_atk_bonus}（{ring_count} 枚） = {hero.atk}"
        )
        st.markdown(
            f"**防禦力**：原始 {hero.base_defense} + 升級 {level_def_bonus} + 武器 {weapon_def_bonus} + 帽子 {hat_def_bonus} + 配件 {accessory_def_bonus} + 戒指 {ring_def_bonus}（{ring_count} 枚） = {hero.defense}"
        )


def render_header():
    st.set_page_config(page_title="幽闇地城", page_icon="🗡️", layout="wide")
    st.title("🕯️ 幽闇地城 ")
    st.caption("選擇職業、探索地城，迎向迷霧試煉。")


def render_status(game):
    hero = game["hero"]
    if not hero:
        st.info("尚未開始冒險。請在左側選擇職業後開始。")
        return

    chapter_label = current_chapter_title(game)
    st.subheader(f"{chapter_label} - 角色狀態")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("角色", f"{hero.icon} {hero.name}")
    col2.metric("職業", hero.class_name)
    col3.metric("等級", f"Lv.{hero.level}")
    col4.metric("金幣", f"💰{hero.gold}")

    col1, col2 = st.columns(2)
    col1.metric("攻擊", hero.atk)
    col2.metric("防禦", hero.defense)

    col1, col2 = st.columns(2)
    with col1:
        render_red_hp_bar(hero.hp, hero.hp_max, f"HP：{hero.hp}/{hero.hp_max}")
    with col2:
        render_blue_mp_bar(hero.mp, hero.mp_max, f"MP：{hero.mp}/{hero.mp_max}")


def render_explore_screen(game):
    hero = game["hero"]
    chapter_label = current_chapter_title(game)
    st.subheader(f"{chapter_label} · 第 {game['floor'] + 1} 層")
    has_enemy = bool(game.get("enemy"))
    explore_button_label = "戰鬥!!" if has_enemy else "繼續探索"
    col1, col2 = st.columns(2)
    with col1:
        if st.button(explore_button_label, use_container_width=True):
            handle_explore("continue")
    with col2:
        if st.button("造訪商人", use_container_width=True, disabled=has_enemy):
            handle_explore("shop")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("就地歇息（💰10）", use_container_width=True, disabled=has_enemy):
            handle_explore("rest")
    with col4:
        if st.button("查看背包", use_container_width=True, disabled=has_enemy):
            handle_explore("inventory")

    st.write("背包：")
    for item_id, item in SHOP_ITEMS.items():
        if item.get("kind") != "consumable":
            continue
        count = hero.inventory.get(item["key"], 0)
        st.write(f"- {item['icon']} {item['name']} × {count}")


def render_battle_screen(game):
    hero = game["hero"]
    enemy = game["enemy"]
    if not hero or not enemy:
        return

    if game.get("battle_turn") == "enemy":
        resolve_enemy_turn(game)
        if hasattr(st, "rerun"):
            st.rerun()
        return

    enemy_icon_display = enemy.icon
    if enemy.is_boss:
        enemy_icon_display = f"<span style='font-size:1.8rem; vertical-align:-0.15rem;'>{enemy.icon}</span>"

    st.markdown("**⚔️ 戰鬥中**")
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<div style='font-size:0.88rem; line-height:1.35; padding-right: 0.5rem;'>"
                    f"<strong>你</strong><br>"
                    f"角色：{hero.icon} {hero.name}<br>"
                    f"職業：{hero.class_name}<br>"
                    f"HP：{hero.hp}/{hero.hp_max}<br>"
                    f"MP：{hero.mp}/{hero.mp_max}<br>"
                    f"攻擊 / 防禦：{hero.atk} / {hero.defense}<br>"
                    f"</div>", unsafe_allow_html=True)
        render_red_hp_bar(hero.hp, hero.hp_max, f"你的 HP：{hero.hp}/{hero.hp_max}")
        render_blue_mp_bar(hero.mp, hero.mp_max, f"你的 MP：{hero.mp}/{hero.mp_max}")
    with col_right:
        st.markdown("<div style='font-size:0.88rem; line-height:1.35; padding-left: 0.5rem;'>"
                    f"<strong>敵人</strong><br>"
                    f"敵人：{enemy_icon_display} {enemy.name}<br>"
                    f"HP：{enemy.hp}/{enemy.hp_max}<br>"
                    f"MP：{enemy.mp}/{enemy.mp_max}<br>"
                    f"攻擊 / 防禦：{enemy.atk} / {enemy.defense}<br>"
                    f"</div>", unsafe_allow_html=True)
        render_red_hp_bar(enemy.hp, enemy.hp_max, f"敵人 HP：{enemy.hp}/{enemy.hp_max}")
        if enemy.mp_max > 0:
            render_blue_mp_bar(enemy.mp, enemy.mp_max, f"敵人 MP：{enemy.mp}/{enemy.mp_max}")

    st.markdown("<div style='font-size:0.92rem; line-height:1.4;'>選擇你的行動：</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⚔️ 攻擊", use_container_width=True, disabled=(game.get("battle_turn") != "player")):
            handle_battle("attack")
    with col2:
        if st.button("✨ 技能", use_container_width=True, disabled=(game.get("battle_turn") != "player")):
            handle_battle("skill")
    with col3:
        if st.button("🏃 逃跑", use_container_width=True, disabled=(game.get("battle_turn") != "player")):
            handle_battle("run")
    with col4:
        if st.button("🎒 背包", use_container_width=True, disabled=(game.get("battle_turn") != "player")):
            pass

    for item_id, item in SHOP_ITEMS.items():
        if item.get("kind") != "consumable":
            continue
        count = hero.inventory.get(item["key"], 0)
        if count > 0 and st.button(f"使用 {item['icon']} {item['name']} × {count}", key=f"use_{item['key']}"):
            handle_battle("item", item["key"])


def render_shop_screen(game):
    hero = game["hero"]
    if not hero:
        return
    st.subheader("🛒 商店")
    st.markdown(
        f"""
        <div style="
            margin: 0.35rem 0 1rem 0;
            padding: 0.6rem 0.9rem;
            font-size: 2rem;
            font-weight: 900;
            line-height: 1.15;
            color: #1f1300;
            background: linear-gradient(90deg, #ffe082 0%, #ffd54f 100%);
            border: 2px solid #f9a825;
            border-radius: 0.65rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
        ">你的金幣：💰{hero.gold}</div>
        """,
        unsafe_allow_html=True,
    )

    section = st.session_state.get("shop_section", "menu")

    if section == "menu":
        st.markdown("### 選擇購買類別")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 藥水補給", key="shop_enter_consumables", use_container_width=True):
                st.session_state["shop_section"] = "consumables"
                if hasattr(st, "rerun"):
                    st.rerun()
        with col2:
            if st.button("🛡️ 裝備鍛造", key="shop_enter_equipment", use_container_width=True):
                st.session_state["shop_section"] = "equipment"
                if hasattr(st, "rerun"):
                    st.rerun()

    elif section == "consumables":
        st.markdown("### 🧪 藥水補給")
        consumables = [
            (item_id, item)
            for item_id, item in SHOP_ITEMS.items()
            if item.get("kind") == "consumable"
        ]

        cols_per_row = 3
        for start in range(0, len(consumables), cols_per_row):
            row_items = consumables[start:start + cols_per_row]
            cols = st.columns(cols_per_row)
            for col_index, (item_id, item) in enumerate(row_items):
                affordable = hero.gold >= item["price"]
                with cols[col_index]:
                    st.markdown(f"**{item['icon']} {item['name']}**")
                    if st.button(
                        f"💰{item['price']} 購買",
                        key=f"buy_{item['key']}",
                        disabled=(not affordable),
                        use_container_width=True,
                    ):
                        buy_item(item_id)
                    st.caption(item["desc"])

        if st.button("返回商店分類", key="shop_back_from_consumables"):
            st.session_state["shop_section"] = "menu"
            if hasattr(st, "rerun"):
                st.rerun()

    else:
        st.markdown("### 🛡️ 裝備鍛造")

        weapon = hero.equipment.get("weapon")
        weapon_level = getattr(hero, "weapon_upgrade_level", 0)
        if weapon:
            st.markdown("#### 🔨 武器強化")
            if weapon_level >= WEAPON_UPGRADE_MAX_LEVEL:
                st.caption(f"{weapon['icon']} {weapon['name']} 已達最高等級 +{weapon_level}")
            else:
                next_level = weapon_level + 1
                cost = WEAPON_UPGRADE_COSTS[next_level]
                current_tag = f"+{weapon_level}"
                next_tag = f"+{next_level}"
                st.markdown(
                    f"<span style='color:#000000;'>{weapon['icon']} {weapon['name']} {current_tag}</span> → {next_tag}"
                    f"（每級 +{WEAPON_UPGRADE_ATK_PER_LEVEL} 攻擊）",
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"強化武器到 {next_tag}（💰{cost}）",
                    key="upgrade_weapon",
                    disabled=(hero.gold < cost),
                ):
                    upgrade_weapon_in_shop()

        st.markdown("#### 🛍️ 裝備商品")
        equipment_items = [
            (item_id, item)
            for item_id, item in SHOP_ITEMS.items()
            if item.get("kind") == "equipment" and item.get("required_class") == hero.class_key
        ]

        cols_per_row = 3
        for start in range(0, len(equipment_items), cols_per_row):
            row_items = equipment_items[start:start + cols_per_row]
            cols = st.columns(cols_per_row)
            for col_index, (item_id, item) in enumerate(row_items):
                affordable = hero.gold >= item["price"]
                is_accessory_item = item.get("slot") != "ring"
                has_any_accessory_equipped = bool(hero.equipment.get("accessory"))
                already_owned_accessory = bool(
                    is_accessory_item
                    and has_any_accessory_equipped
                )
                label = f"購買 {item['icon']} {item['name']}（💰{item['price']}）"
                if already_owned_accessory:
                    label = f"已裝備配件，無法購買 {item['icon']} {item['name']}"

                with cols[col_index]:
                    st.markdown(f"**{item['icon']} {item['name']}**")
                    if st.button(
                        label,
                        key=f"buy_{item['key']}",
                        disabled=(not affordable or already_owned_accessory),
                        use_container_width=True,
                    ):
                        buy_item(item_id)
                    st.caption(item["desc"])
                    if item.get("slot") == "ring":
                        st.caption("✅ 可重複購買，效果疊加")
                    if item.get("kind") == "equipment":
                        required = CLASSES[next((k for k, v in CLASSES.items() if v["key"] == item["required_class"]), "1")]
                        st.caption(f"職業限定：{required['icon']} {required['name']}")

        if st.button("返回商店分類", key="shop_back_from_equipment"):
            st.session_state["shop_section"] = "menu"
            if hasattr(st, "rerun"):
                st.rerun()
    if st.button("離開商店"):
        game["phase"] = "explore"
        st.session_state["shop_section"] = "menu"
        save_game(game)
        if hasattr(st, "rerun"):
            st.rerun()


def render_inventory_screen(game):
    hero = game["hero"]
    if not hero:
        return
    st.subheader("🎒 背包")
    for item_id, item in SHOP_ITEMS.items():
        if item.get("kind") != "consumable":
            continue
        count = hero.inventory.get(item["key"], 0)
        st.write(f"- {item['icon']} {item['name']} × {count} — {item['desc']}")
    if st.button("返回探索"):
        game["phase"] = "explore"
        save_game(game)


def render_chapter_complete(game):
    hero = game["hero"]
    chapter = game.get("chapter", 1)
    if chapter == 1:
        st.success("第一章完結：幽闇地城已被淨化。")
        st.write("你獲得了片刻的平靜，但遠方的迷霧仍在呼喚你。")
        if st.button("進入第二章：深淵之外"):
            start_chapter_two(game)
            if hasattr(st, "rerun"):
                st.rerun()
    else:
        st.success("第二章完結：迷霧已被突破。")
        st.write("你已走過迷霧深處，幽冥之巔的最終考驗即將展開。")
        if st.button("進入第三章：幽冥之巔"):
            start_chapter_three(game)
            if hasattr(st, "rerun"):
                st.rerun()


def render_game_over(game):
    st.error("你倒下了……")
    if st.button("重新開始"):
        start_new_game()


def render_victory(game):
    hero = game["hero"]
    st.success("🎉✨ 深淵已淨化 ✨🎉")
    st.markdown(
        f"你以 Lv.{hero.level} 的 **{hero.name}** 之姿，踏著黎明前的微光走出地城。"
    )
    st.markdown("火把一盞盞點亮，城門前爆出歡呼，鐘聲與花火在夜空中交織。 🏰🎆")
    st.markdown("旅人傳頌你的戰歌，孩童高喊你的名字，而黑夜終於學會了退去。 🕊️🌅")


def main():
    ensure_game_state()
    render_header()
    left_col, center_col, right_col = st.columns([1.1, 2.0, 1.2], gap="large")

    with left_col:
        render_left_panel()

    game = st.session_state.game
    game.setdefault("battle_turn", "player")
    with center_col:
        if game["phase"] not in ("battle", "shop"):
            render_status(game)

        if game["phase"] == "start":
            st.info("選擇職業並開始冒險。")
        elif game["phase"] == "explore":
            render_explore_screen(game)
        elif game["phase"] == "battle":
            render_battle_screen(game)
        elif game["phase"] == "shop":
            render_shop_screen(game)
        elif game["phase"] == "inventory":
            render_inventory_screen(game)
        elif game["phase"] == "gameover":
            render_game_over(game)
        elif game["phase"] == "chapter_complete":
            render_chapter_complete(game)
        elif game["phase"] == "victory":
            render_victory(game)

    with right_col:
        st.subheader("📝 冒險紀錄")
        boss_encounter_messages = {
            "👑 深淵王甦醒，注視著你……",
            "🌫️ 霧中巨影現身，迷霧領主向你發出冷笑……",
            "👑 幽冥王座震顫，幽冥領主現身，黑焰席捲四方……",
        }
        if game["messages"]:
            for message in reversed(game["messages"]):
                if message in boss_encounter_messages:
                    st.markdown(f"**{message}**")
                else:
                    st.write(message)
        else:
            st.write("尚無冒險紀錄。")


if __name__ == "__main__":
    main()