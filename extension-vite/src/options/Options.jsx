import { useFormik } from 'formik'
import { useEffect, useState } from 'react'
import { Button, Card, Col, Container, Form, OverlayTrigger, Row, Tooltip } from 'react-bootstrap'
import Swal from 'sweetalert2'
import * as Yup from 'yup'
import api from '../api'
import { CircleQuestion } from '../components/Svg'
import constants from '../core/constants'
import { isApiSuccess } from '../utils/api-call'
import './Options.css'

function App() {
  const [task, setTask] = useState({
    urlRule: '',
    taskName: '',
    id: '',
    accessKey: '',
    taskStatusId: '',
  })
  const [isLoading, setIsLoading] = useState(true)
  const [shouldRefresh, setShouldRefresh] = useState(false)

  useEffect(() => {
    const fetchFirstTask = async () => {
      const response = await api.getCurrentTask()

      // Check if the response was successful and a task was returned
      if (response && isApiSuccess(response) && response.data) {
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
      }
      setIsLoading(false) // After checking for the existing task, set isLoading to false
    }

    fetchFirstTask()
  }, [shouldRefresh])

  const isNewTask = !(
    task.id &&
    (task.taskStatusId === constants.TASK_STATUS.WAITING ||
      task.taskStatusId === constants.TASK_STATUS.PAUSED ||
      task.taskStatusId === constants.TASK_STATUS.RUNNING)
  )

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      taskName: '',
      urlRule: '',
      // email: '',
      ...task,
    },
    validationSchema: Yup.object({
      taskName: Yup.string().max(255).required('Task name is required'),
      urlRule: Yup.string()
        .max(100, 'Maximum length is 100 characters')
        .required('URL Rule is required'),
      // email: Yup.string().email('Invalid email format').max(255),
    }),
    onSubmit: async (values, helpers) => {
      const { taskName, urlRule, id } = values
      let response

      // If it's a new task
      if (isNewTask) {
        response = await api.createTask({
          taskName,
          urlRule,
        })
      } else {
        // If it's an existing task
        response = await api.updateTask({
          id,
          taskName,
          urlRule,
        })
      }

      if (!isApiSuccess(response)) {
        console.log('Error when submitting task!', response.error)
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: `Failed to ${isNewTask ? 'create' : 'update'} the task!`,
        }).then(() => {
          window.location.reload() // refresh the page just in case the user is logged out
        })
        return
      }

      console.log(`${isNewTask ? 'Created' : 'Updated'} Task!`, response.data)

      // const { access_key: accessKey, id: taskId, task_status_id: taskStatusId } = response.data
      // saveTaskToStorage({
      //   urlRule,
      //   taskName,
      //   id: taskId,
      //   accessKey,
      //   taskStatusId,
      // })
      Swal.fire({
        icon: 'success',
        title: `Task ${isNewTask ? 'created' : 'updated'} successfully`,
        showConfirmButton: true,
        timer: 5000,
      })
      setShouldRefresh(!shouldRefresh)
    },
  })

  const renderURLTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props}>
      You can use the asterisk (*) in any URL segment to match certain patterns. For example,
      http://*.example.com/*
    </Tooltip>
  )

  // If isLoading is true, don't render anything.
  if (isLoading) {
    return null
  }

  const hasRunningTask = task.taskStatusId && task.taskStatusId === constants.TASK_STATUS.RUNNING

  return (
    <main>
      <Container>
        <Card
          className="text-center shadow-sm"
          style={{
            maxWidth: '80%',
            margin: 'auto',
          }}
        >
          <Card.Body className="p-5">
            <Card.Title>
              <img
                src="/img/logo-128.png"
                alt="logo"
                style={{
                  width: '2.8rem',
                  margin: '0 0.5rem 0.5rem 0',
                }}
              />
              {isNewTask ? 'New' : 'Edit'} Task Configurations
            </Card.Title>
            <hr />
            <Form
              className="text-start"
              noValidate
              onSubmit={(e) => {
                e.preventDefault()
                formik.handleSubmit(e)
              }}
            >
              <Form.Group as={Row} className="mb-3" controlId="formHorizontalTaskName">
                {!isNewTask && (
                  <Form.Group as={Row} className="mb-3" controlId="formHorizontalStatus">
                    <Form.Label column sm={2}>
                      Task Status
                    </Form.Label>
                    <Form.Label column sm={10}>
                      {constants.TASK_STATUS_NAME[task?.taskStatusId]}
                    </Form.Label>
                  </Form.Group>
                )}
                <Form.Label column sm={2}>
                  Task Name
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="text"
                    placeholder="Task Name"
                    name="taskName"
                    value={formik.values.taskName}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    isInvalid={formik.touched.taskName && !!formik.errors.taskName}
                    disabled={hasRunningTask}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formik.errors.taskName}
                  </Form.Control.Feedback>
                </Col>
              </Form.Group>
              <Form.Group as={Row} className="mb-3" controlId="formHorizontalURL">
                <Form.Label column sm={2}>
                  URL
                  <OverlayTrigger
                    // placement="right"
                    overlay={renderURLTooltip}
                  >
                    <div className="d-inline-flex mx-1">
                      <CircleQuestion height="0.9rem" />
                    </div>
                  </OverlayTrigger>
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="text"
                    placeholder="http://xxx.xx.com/*"
                    name="urlRule"
                    value={formik.values.urlRule}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    isInvalid={formik.touched.urlRule && !!formik.errors.urlRule}
                    disabled={hasRunningTask}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formik.errors.urlRule}
                  </Form.Control.Feedback>
                </Col>
              </Form.Group>
              {/* <Form.Group as={Row} className="mb-3" controlId="formHorizontalEmail">
                <Form.Label column sm={2}>
                  Email
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="email"
                    placeholder="for notification purpose: e.g. john@doe.com"
                    name="email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    isInvalid={formik.touched.email && !!formik.errors.email}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formik.errors.email}
                  </Form.Control.Feedback>
                </Col>
              </Form.Group> */}
              <Form.Group as={Row} className="mb-3" controlId="formHorizontalVersion">
                <Form.Label column sm={2}>
                  App Version
                </Form.Label>
                <Form.Label column sm={10}>
                  {import.meta.env.VITE_API_VERSION}
                </Form.Label>
              </Form.Group>
              <Row className="mb-3">
                <Col sm={12}>
                  <Button
                    type="submit"
                    className="w-100"
                    disabled={formik.isSubmitting || hasRunningTask}
                  >
                    {isNewTask ? 'Create New Task' : 'Edit Task'}
                  </Button>
                  {hasRunningTask && (
                    <div className="mt-2 text-danger">
                      Note: Settings cannot be modified while the task is running.
                    </div>
                  )}
                </Col>
              </Row>
            </Form>
          </Card.Body>
        </Card>
      </Container>
    </main>
  )
}

export default App
