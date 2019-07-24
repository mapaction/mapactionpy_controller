# flake8: noqa
csv_06_source_lookup = r"""
Value,Organisation,url,admn1Name,admn1PCode,admn2Name,admn2PCode
ma,MapAction,,admn1Name,admn1PCode,admn2Name,admn2PCode
statoid,Statoid: data on admin units,,NameAdmin1,NamePCode,Name2_admin,Name2_pocde
undac,UN Disaster Assessment Coordination,,,,,
uniom,UN International Organization for Migration,,,,,
"""

csv_06_source_lookup_duplicate_prikey = r"""
Value,Organisation,url,admn1Name,admn1PCode,admn2Name,admn2PCode
ma,MapAction,,admn1Name,admn1PCode,admn2Name,admn2PCode
statoid,Statoid: data on admin units,,NameAdmin1,NamePCode,Name2_admin,Name2_pocde
undac,UN Disaster Assessment Coordination,,,,,
undac,UN Disaster Assessment Coordination,,,,,
uniom,UN International Organization for Migration,,,,,
"""
