
module Rede.Http2.MakeAttendant (
    http2Attendant
    ) where


import           Rede.Http2.Framer            (wrapSession)
import           Rede.MainLoop.CoherentWorker
import           Rede.MainLoop.PushPullType   (CloseAction, PullAction,
                                               PushAction)



http2Attendant :: CoherentWorker -> PushAction -> PullAction -> CloseAction ->  IO ()
http2Attendant coherent_worker push_action pull_action  close_action = do 
    let 
        attendant = wrapSession coherent_worker
    attendant push_action pull_action close_action    