## static/js/reducers.js

// Global variables
const initialState = {
  users: [],
  goals: [],
  recommendations: [],
  notifications: [],
  reminders: [],
};

// User reducer
const userReducer = (state = initialState.users, action) => {
  switch (action.type) {
    case "CREATE_USER":
      return [...state, action.payload];
    default:
      return state;
  }
};

// Goal reducer
const goalReducer = (state = initialState.goals, action) => {
  switch (action.type) {
    case "CREATE_GOAL":
      return [...state, action.payload];
    case "UPDATE_PROGRESS":
      return state.map((goal) =>
        goal.id === action.payload.id ? { ...goal, progress: action.payload.progress } : goal
      );
    case "DELETE_GOAL":
      return state.filter((goal) => goal.id !== action.payload);
    default:
      return state;
  }
};

// Recommendation reducer
const recommendationReducer = (state = initialState.recommendations, action) => {
  switch (action.type) {
    case "CREATE_RECOMMENDATION":
      return [...state, action.payload];
    default:
      return state;
  }
};

// Notification reducer
const notificationReducer = (state = initialState.notifications, action) => {
  switch (action.type) {
    case "CREATE_NOTIFICATION":
      return [...state, action.payload];
    default:
      return state;
  }
};

// Reminder reducer
const reminderReducer = (state = initialState.reminders, action) => {
  switch (action.type) {
    case "CREATE_REMINDER":
      return [...state, action.payload];
    default:
      return state;
  }
};

export const rootReducer = {
  users: userReducer,
  goals: goalReducer,
  recommendations: recommendationReducer,
  notifications: notificationReducer,
  reminders: reminderReducer,
};
