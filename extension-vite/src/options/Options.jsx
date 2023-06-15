import { useFormik } from 'formik'
import { Button, Card, Col, Container, Form, Row } from 'react-bootstrap'
import * as Yup from 'yup'
import './Options.css'

function App() {
  const formik = useFormik({
    initialValues: {
      taskName: '',
      urlRegex: '',
      email: '',
    },
    validationSchema: Yup.object({
      taskName: Yup.string().max(255).required('Task name is required'),
      urlRegex: Yup.string().max(255).required('URL Regex is required'),
      email: Yup.string().email('Invalid email format').max(255),
    }),
    onSubmit: async (values, helpers) => {
      // TODO: submit logic here
      console.log('Hi submitted', values)
    },
  })

  const isNewTask = true // TODO: check if is new task

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
                      Status
                    </Form.Label>
                    <Form.Label column sm={10}>
                      No Running Task
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
                  />
                  <Form.Control.Feedback type="invalid">
                    {formik.errors.taskName}
                  </Form.Control.Feedback>
                </Col>
              </Form.Group>
              <Form.Group as={Row} className="mb-3" controlId="formHorizontalURL">
                <Form.Label column sm={2}>
                  URL Regex
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="text"
                    placeholder="http://xxx.xx.com/*"
                    name="urlRegex"
                    value={formik.values.urlRegex}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    isInvalid={formik.touched.urlRegex && !!formik.errors.urlRegex}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formik.errors.urlRegex}
                  </Form.Control.Feedback>
                </Col>
              </Form.Group>
              <Form.Group as={Row} className="mb-3" controlId="formHorizontalEmail">
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
              </Form.Group>
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
                  <Button type="submit" className="w-100">
                    {isNewTask ? 'Create New Task' : 'Edit Task'}
                  </Button>
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
