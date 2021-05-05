# lutil-s3-text-lines-to-sns




# Fanning Out Tasks

```
*Producer                    *Handler                 *Consumer
            fan_out-->
                                    task_created-->
                                    
                                    <--task started

                                    <--task completed
                                    <--task error

            <--task completed
```

