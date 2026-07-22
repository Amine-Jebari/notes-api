output "bucket_name" {
  value = aws_s3_bucket.notes_storage.id
}

output "queue_url" {
  value = aws_sqs_queue.notes_events.url
}

output "queue_arn" {
  value = aws_sqs_queue.notes_events.arn
}

output "table_arn" {
  value = aws_dynamodb_table.notes_table.arn
}