server <- function(input, output){
	selected_data <- reactive({
        	# Connect to the DB
        	conn <- dbConnect(
                  RPostgres::Postgres(),
                  dbname = "hjkim",
                  host = "172.18.0.3",
                  port = "5432",
                  user = "hjkim",
                  password = "hjkim"
		)
        	# Get the data
        	corona <- dbGetQuery(conn, glue("SELECT s_dt, n_hj::integer as n_hj, replace(t_hj,'.','')::integer as t_hj FROM tb WHERE s_dt BETWEEN '{format(input$dates[1])}' AND '{format(input$dates[2])}'"))
        	# Disconnect from the DB
        	dbDisconnect(conn)
        	# Convert to data.frame
        	data.frame(corona)
	})
	
	output$plot <- renderPlot({
		ggplot(data=selected_data(), aes(x=s_dt, y=n_hj)) + 
			geom_line(color='blue', linewidth = 1) + 
			geom_point(color='red') + 
			geom_smooth(method='lm') +
			ggtitle("Daily confirmed cases") +
			labs(x='Date',y='Daily confirmed cases')
	})
	output$t_hj <- renderPlot({
               ggplot(data=selected_data(), aes(x=s_dt, y=t_hj)) +
               geom_line(color='blue', linewidth = 1) +
               geom_point(color='red') +
               geom_smooth(method='lm') +
	       ggtitle("Total confirmed cases") +
               labs(x='Date',y='Total confirmed cases')
        })

}
