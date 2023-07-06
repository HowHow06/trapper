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
import { sendRuntimeMessagePromise } from '../utils/chromeMessage'
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

  const getTaskToStart = (taskFromApi) => {
    const {
      task_status_id: taskStatusId,
      task_name: taskName,
      url_rule: urlRule,
      id: id,
      access_key: accessKey,
    } = taskFromApi

    const taskToStart = {
      urlRule,
      taskName,
      id,
      accessKey,
      taskStatusId,
    }
    return taskToStart
  }

  useEffect(() => {
    const initialize = async () => {
      const fetchFirstTask = async () => {
        const response = await api.getCurrentTask()
        // Check if the response was successful and a task was returned
        if (response && response.data) {
          const task = response.data
          const taskForState = getTaskToStart(task)
          setTask(taskForState)
          console.log('hi task!', taskForState)

          if (taskForState.taskStatusId === constants.TASK_STATUS.RUNNING) {
            // restart the task if the current task is running whenever the popup is opened
            sendRuntimeMessagePromise({
              actionName: constants.MESSAGE_ACTION_NAME.START_TASK,
              task: taskForState,
            })
          }
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

      if (ignore.current) {
        return
      }

      ignore.current = true

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

    const taskToStart = getTaskToStart(response.data.task)
    // save task to storage here, so that the event listener can get the value
    // saveTaskToStorage(taskToStart)

    // TODO: add listener here
    sendRuntimeMessagePromise({
      actionName: constants.MESSAGE_ACTION_NAME.START_TASK,
      task: taskToStart,
    })

    // chrome.notifications.create(
    //   'notify1',
    //   {
    //     type: 'basic',
    //     iconUrl: 'icons/logo.ico',
    //     title: `Operation Succeed!`,
    //     message: `Demo notification Message here`,
    //     contextMessage: 'Task started successfully.',
    //   },
    //   () => {

    //     console.log("Error:", chrome.runtime.lastError)
    //     console.log('noti functions callback')
    //   },
    // )

    ignore.current = false
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

    // clearAllStorageData()
    // TODO: remove listener here
    sendRuntimeMessagePromise({ actionName: constants.MESSAGE_ACTION_NAME.STOP_TASK })

    ignore.current = false
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
        <PauseTaskButton
          onClick={() => {
            sendRuntimeMessagePromise({
              actionName: constants.MESSAGE_ACTION_NAME.START_TASK,
              task: task,
            })
          }}
        />
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
