// Project Horizon - Survey Charter client side (hand-written, 0.6.1).
// The server script owns the charter panel. On the client, a right-click on the charter is consumed here so the client
// does not go on to use the off-hand item (vanilla tries the off hand when the main-hand use on a plain block passes).
// The main-hand ServerboundUseItemOn packet is still sent (NeoForge posts this event inside the prediction that builds
// the packet), so the server panel opens as before. cancel() throws EventExit: it must stay the last statement.
BlockEvents.rightClicked('horizon:survey_charter', event => {
  event.cancel()
})
