import { useEffect, useRef, useState } from 'react'
import { Stack } from 'react-bootstrap'
import api from '../api'
import BaseActionButton from '../components/BaseActionButton'
import { LoadingSpinner } from '../components/LoadingSpinner'
import LoginPrompt from '../components/LoginPrompt'
import PopupContainer from '../components/PopupContainer'
import { ArrowUpRight, Pause, Play, Stop } from '../components/Svg'
import constants from '../core/constants'
import { isApiSuccess } from '../utils/api-call'
import './Popup.css'

function App() {
  const ignore = useRef(false)
  const [task, setTask] = useState({
    urlRule: '',
    taskName: '',
    id: '',
    accessKey: '',
    taskStatusId: '',
  }) // TODO: use custom hook instead
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [shouldRefresh, setShouldRefresh] = useState(false)

  useEffect(() => {
    const initialize = async () => {
      const fetchFirstTask = async () => {
        const response = await api.getCurrentTask()
        // Check if the response was successful and a task was returned
        if (response && response.data) {
          const task = response.data
          const {
            url_rule: urlRule,
            task_name: taskName,
            id,
            access_key: accessKey,
            task_status_id: taskStatusId,
          } = task
          setTask({ urlRule, taskName, id, accessKey, taskStatusId })
          console.log('hi task!', { urlRule, taskName, id, accessKey, taskStatusId })
        } else {
          console.log('no task!')
          setTask({
            urlRule: '',
            taskName: '',
            id: '',
            accessKey: '',
            taskStatusId: '',
          })
        }
      }

      const testToken = async () => {
        const response = await api.testToken()
        if (isApiSuccess(response)) {
          console.log('Legit User!', response.data)
          setIsLoggedIn(true)
        } else {
          console.log('Test Token failed', response.error)
          setIsLoggedIn(false)
        }
      }

      await Promise.all([fetchFirstTask(), testToken()])

      setIsLoading(false)
    }

    initialize()
  }, [shouldRefresh])

  const hasCurrentTask = Boolean(task.id)
  const hasCurrentRunningTask =
    hasCurrentTask && task.taskStatusId === constants.TASK_STATUS.RUNNING

  const handleSettingClick = () => {
    chrome.runtime.openOptionsPage()
  }

  // If isLoading is true, don't render anything.
  if (isLoading) {
    return (
      <div className="m-3">
        <LoadingSpinner />
      </div>
    )
  }

  if (!isLoggedIn) {
    return (
      <PopupContainer>
        <LoginPrompt />
      </PopupContainer>
    )
  }

  const startCurrentTask = async () => {
    const response = await api.startTask({
      id: task.id,
    })

    if (!isApiSuccess(response)) {
      console.log('Error when starting task!', response.error)
      return
    }

    // TODO: add listener here
    setShouldRefresh(!shouldRefresh)
  }

  const stopCurrentTask = async () => {
    const response = await api.stopTask({
      id: task.id,
    })

    if (!isApiSuccess(response)) {
      console.log('Error when stoping task!', response.error)
      return
    }

    // TODO: remove listener here
    setShouldRefresh(!shouldRefresh)
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

  const StopTaskButton = ({ ...rest }) => {
    return (
      <BaseActionButton
        className="btn-danger"
        icon={<Stop height="1rem" color="#ffffff" />}
        text={'Stop Task'}
        {...rest}
      />
    )
  }

  return (
    <PopupContainer>
      <Stack gap={2}>
        {hasCurrentRunningTask ? (
          <>
            {/* {isTaskRunning ? (
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
            )} */}
            <StopTaskButton onClick={stopCurrentTask} />
          </>
        ) : (
          <>
            <StartTaskButton onClick={startCurrentTask} disabled={!isLoggedIn || !hasCurrentTask} />
            {!hasCurrentTask && (
              <span className="text-label text-primary">
                * Please complete the task configuration at settings page
              </span>
            )}
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
