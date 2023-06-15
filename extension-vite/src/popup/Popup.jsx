import { useState } from 'react'
import { Stack } from 'react-bootstrap'
import BaseActionButton from '../components/BaseActionButton'
import LoginPrompt from '../components/LoginPrompt'
import PopupContainer from '../components/PopupContainer'
import { ArrowUpRight, Pause, Play, Stop } from '../components/Svg'
import './Popup.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true)
  const [isHasCurrentTask, setIsHasCurrentTask] = useState(false)
  const [isTaskRunning, setIsTaskRunning] = useState(true)
  const [isConfigurationReady, setIsConfigurationReady] = useState(false)

  const handleSettingClick = () => {
    chrome.runtime.openOptionsPage()
  }

  if (!isLoggedIn) {
    return (
      <PopupContainer>
        <LoginPrompt />
      </PopupContainer>
    )
  }

  const PauseTaskButton = ({ ...rest }) => {
    return (
      <BaseActionButton
        icon={<Pause height="1rem" color="#ffffff" />}
        text={'Pause Task'}
        {...rest}
      />
    )
  }

  const StartTaskButton = ({ ...rest }) => {
    return (
      <BaseActionButton
        icon={<Play height="1rem" color="#ffffff" />}
        text={'Start Task'}
        {...rest}
      />
    )
  }

  const ResumeTaskButton = ({ ...rest }) => {
    return (
      <BaseActionButton
        icon={<Play height="1rem" color="#ffffff" />}
        text={'Resume Task'}
        {...rest}
      />
    )
  }

  const StopTaskButton = () => {
    return (
      <BaseActionButton
        className="btn-danger"
        icon={<Stop height="1rem" color="#ffffff" />}
        text={'Stop Task'}
      />
    )
  }

  return (
    <PopupContainer>
      <Stack gap={2}>
        {!isHasCurrentTask ? (
          <>
            <StartTaskButton
              onClick={() => {
                console.log('StartTaskButton')
              }}
              disabled={!isConfigurationReady}
            />
            <span className="text-label text-primary">
              * Please complete the task configuration at settings page
            </span>
          </>
        ) : (
          <>
            {isTaskRunning ? (
              <PauseTaskButton
                onClick={() => {
                  console.log('PauseTaskButton')
                }}
              />
            ) : (
              <ResumeTaskButton
                onClick={() => {
                  console.log('ResumeTaskButton')
                }}
              />
            )}
            <StopTaskButton
              onClick={() => {
                console.log('StopTaskButton')
              }}
            />
          </>
        )}
        <div>
          <hr />
          <Stack
            direction="horizontal"
            gap={2}
            className="w-100 justify-content-center on-hover-pointer"
            onClick={handleSettingClick}
          >
            <p className="m-0">Go to settings</p>
            <ArrowUpRight height="0.8rem" />
          </Stack>
        </div>
      </Stack>
    </PopupContainer>
  )
}

export default App
