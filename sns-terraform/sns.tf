variable "fifo_topic" {
  description = "Indicates whether the topic is a FIFO topic."
  type        = bool
  default     = false
}

variable "topic_name" {
  description = "The name of the SNS topic"
  type        = string
}

variable "content_based_deduplication" {
  description = "Enables content-based deduplication for FIFO topics."
  type        = bool
  default     = false
}

resource "aws_sns_topic" "my_topic" {
  name                      = var.fifo_topic ? "${var.topic_name}.fifo" : var.topic_name
  fifo_topic                = var.fifo_topic

  // Only set content_based_deduplication if fifo_topic is true
  content_based_deduplication = var.fifo_topic ? var.content_based_deduplication : null

  // Other topic properties can be added here
}

resource "null_resource" "fail_if_non_fifo_with_deduplication" {
  count = (!var.fifo_topic && var.content_based_deduplication) ? 1 : 0

  provisioner "local-exec" {
    command = "echo 'Error: Content-based deduplication can only be set for FIFO topics.' && exit 1"
  }
}

output "fifo_topic_status" {
  value = aws_sns_topic.my_topic.fifo_topic
}

output "content_based_deduplication_status" {
  value = aws_sns_topic.my_topic.content_based_deduplication
}