from django.db import models


# Create your models here.


class NovelCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name="分类名称", unique=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "小说分类"
        verbose_name_plural = verbose_name
        db_table = "tb_novel_category"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name="名称", unique=True)
    intro = models.CharField(max_length=255, verbose_name="简介", default="")
    image = models.ImageField(upload_to="authors/", max_length=200, verbose_name="作者图片", default="default_author.jpg",
                              null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "小说作者"
        verbose_name_plural = verbose_name
        db_table = "tb_novel_author"

    def __str__(self):
        return self.name


class Novel(models.Model):
    novel_name = models.CharField(unique=True, max_length=32, verbose_name="小说名称")
    site_name = models.CharField(max_length=32, verbose_name="小说网站")
    url = models.CharField(unique=True, max_length=255, verbose_name="小说链接")
    category = models.ForeignKey(NovelCategory, models.CASCADE, verbose_name="小说分类")
    image = models.ImageField(upload_to='novel/', max_length=200, verbose_name="小说图片", default="default_novel.jpg",
                              null=True, blank=True)
    author = models.ForeignKey(Author, models.CASCADE, verbose_name="小说作者")
    intro = models.TextField(verbose_name="小说简介", default="")
    read_nums = models.PositiveIntegerField(default=0, verbose_name="阅读数")
    fav_nums = models.PositiveIntegerField(default=0, verbose_name="收藏数")
    parser = models.CharField(max_length=255, default="biqugeParser", verbose_name="内容解析器")
    enable = models.BooleanField(verbose_name="是否显示", default=True)
    is_end = models.BooleanField(verbose_name="是否已完结", default=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "小说"
        verbose_name_plural = verbose_name
        db_table = 'tb_novel'

    def __str__(self):
        return self.novel_name


class Chapter(models.Model):
    obj_id = models.CharField(max_length=64, verbose_name="url的MD5", primary_key=True)
    novel = models.ForeignKey('Novel', models.CASCADE, verbose_name="小说")
    url = models.URLField(unique=True, max_length=255, verbose_name="章节链接")
    index = models.PositiveIntegerField(verbose_name="章节顺序", default=0)
    name = models.CharField(max_length=255, verbose_name="章节名称")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "tb_chapter"

    def __str__(self):
        return self.name
