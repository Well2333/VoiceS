class Config:

    """Slice Setting"""

    Slice_warning_min_sec: int = 2
    Slice_recommand_min_sec: int = 5
    Slice_warning_max_sec: int = 20
    Slice_recommand_max_sec: int = 15

    """pinyin setting"""
    pinyin_heteronym_check: bool = True


config: Config = Config()
