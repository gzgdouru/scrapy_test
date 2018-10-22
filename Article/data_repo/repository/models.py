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
