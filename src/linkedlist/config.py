import os, os.path

base_path = os.getcwd()

DATABASE = os.path.join(base_path, "linkedlist.db")
DEBUG = True
SECRET_KEY = "7B+PL102DpIf5bULXiER1t/dqsf1uLmqSmdjNR8L1+Q2MFnlNL93Ij09p2fxB6gw5mMh2Mmu4UG3G5UR6b9org"

admin_pw_hash = "pbkdf2:sha512:1000$Ygm5mN6e$c04bd6ce8332a5a5958d1d1b6ec3d90d7c7b576c0ff1f12e5a3cd4e778c7b4d737dd9e9361d5899f5f0d8fb631654b8af8f6c81813c2cf8e13f8ba655ce4b8aa"
