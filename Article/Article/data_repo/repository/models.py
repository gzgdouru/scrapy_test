from django.db import models

# Create your models here.


class JobboleArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    create_date = models.DateField(verbose_name="创建时间", null=True, blank=True)
    url = models.URLField(max_length=255, verbose_name="url")
    url_object_id = models.CharField(max_length=64, verbose_name="url标识", primary_key=True)
    front_image_url = models.URLField(max_length=255, verbose_name="封面图url", null=True, blank=True)
    front_image_path = models.CharField(max_length=255, verbose_name="封面图存放路径", null=True, blank=True)
    praise_nums = models.PositiveIntegerField(verbose_name="点赞数", default=0)
    fav_nums = models.PositiveIntegerField(verbose_name="收藏数", default=0)
    comment_nums = models.PositiveIntegerField(verbose_name="评论数", default=0)
    content = models.TextField(verbose_name="内容", null=True, blank=True)
    tags = models.CharField(max_length=255, verbose_name="标签", null=True, blank=True)

    class Meta:
        db_table = "tb_jobbole_article"

    def __str__(self):
        return self.title


class ZhihuQuestion(models.Model):
    zhihu_id = models.BigIntegerField(verbose_name="知乎提问id", primary_key=True)
    topics = models.CharField(max_length=255, verbose_name="专题", null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name="url")
    title = models.CharField(max_length=255, verbose_name="标签")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True, blank=True)
    answer_num = models.PositiveIntegerField(verbose_name="回答数", default=0)
    comments_num = models.PositiveIntegerField(verbose_name="评论数", default=0)
    watch_user_num = models.PositiveIntegerField(verbose_name="浏览数", default=0)
    click_num = models.PositiveIntegerField(verbose_name="点击数", default=0)
    crawl_time = models.DateTimeField(verbose_name="爬虫派取时间")
    crawl_update_time = models.DateTimeField(verbose_name="爬虫更新时间", null=True, blank=True)

    class Meta:
        db_table = "tb_zhihu_question"

    def __str__(self):
        return self.title


class ZhihuAnswer(models.Model):
    zhihu_id = models.BigIntegerField(verbose_name="知乎回答id", primary_key=True)
    url = models.CharField(max_length=255, verbose_name="url")
    question = models.ForeignKey(ZhihuQuestion, on_delete=models.CASCADE, verbose_name="知乎提问")
    author_id = models.CharField(max_length=128, verbose_name="作者id", null=True, blank=True)
    content = models.TextField(verbose_name="内容")
    praise_num = models.PositiveIntegerField(verbose_name="点赞数", default=0)
    comments_num = models.PositiveIntegerField(verbose_name="评论数", default=0)
    create_time = models.DateTimeField(verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="更新时间")
    crawl_time = models.DateTimeField(verbose_name="爬虫派取时间")
    crawl_update_time = models.DateTimeField(verbose_name="爬虫更新时间", null=True, blank=True)

    class Meta:
        db_table = 'tb_zhihu_answer'

    def __str__(self):
        return "{0}/{1}".format(self.question, self.zhihu_id)


class LagouJob(models.Model):
    obj_id = models.CharField(max_length=64, verbose_name="url的md5", primary_key=True)
    url = models.URLField(max_length=255, verbose_name="url")
    title = models.CharField(max_length=255, verbose_name="标题")
    salary_min = models.PositiveIntegerField(verbose_name="最低薪资", default=0)
    salary_max = models.PositiveIntegerField(verbose_name="最高薪资", default=0)
    job_city = models.CharField(max_length=16, verbose_name="工作城市", null=True, blank=True)
    work_years_min = models.PositiveIntegerField(verbose_name="最低工作年限", default=0)
    work_years_max = models.PositiveIntegerField(verbose_name="最高工作年限", default=0)
    degree_need = models.CharField(max_length=32, verbose_name="学历", null=True, blank=True)
    job_type = models.CharField(max_length=32, verbose_name="工作类型", null=True, blank=True)
    publish_time = models.DateTimeField(verbose_name="发布时间")
    tags = models.CharField(max_length=255, verbose_name="标签", null=True, blank=True)
    job_advantage = models.CharField(max_length=1024, verbose_name="职位诱惑", null=True, blank=True)
    job_desc = models.TextField(verbose_name="职位描述")
    job_addr = models.CharField(max_length=64, verbose_name="工作地点", null=True, blank=True)
    company_url = models.URLField(max_length=255, verbose_name="公司链接", null=True, blank=True)
    company_name = models.CharField(max_length=255, verbose_name="公司名称", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = 'tb_lagou_job'

    def __str__(self):
        return self.title