import pusher

pusher_client = pusher.Pusher(
  app_id='853461',
  key='7443318dffd154df2e7d',
  secret='ddfc4d7fd9521374a4c6',
  cluster='eu'
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
