output "bucket_name" {
  value = aws_s3_bucket.notes.id
}

output "queue_url" {
  value = aws_sqs_queue.notes_events.url
}

output "queue_arn" {
  value = aws_sqs_queue.notes_events.arn
}