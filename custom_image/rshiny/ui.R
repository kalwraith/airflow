ui <- fluidPage(
	tags$h1("corona19"),
	sidebarPanel(
		textInput("사망자","확진자"),
		dateRangeInput("dates",
			       "Date range",
			       start = as.Date("2023-01-01"),
			       end = Sys.Date()),
		br(),
		br()
	),
	mainPanel(plotOutput("plot"), plotOutput("t_hj"))
)

