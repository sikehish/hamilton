import React, { useState, createContext } from "react";
import { useLocalStorage } from "../utils/localStorage";
import { HiChevronDown, HiChevronUp } from "react-icons/hi";

type UserContextType = {
  username: string;
  setUsername: (username: string) => void;
  userAPIKey: string | undefined;
};

// Creating a context with a default value and type annotation
export const UserContext = createContext<UserContextType | undefined>(
  undefined
);

export const LocalLoginProvider = (props: { children: React.ReactNode }) => {
  const [localUsername, setLocalUsername] = useState<string>("");
  const [keyInputExpanded, setKeyInputExpanded] = useState(false);

  const [username, setUsername] = useLocalStorage(
    "hamilton-username",
    undefined
  );
  const [apiKey, setApiKey] = useLocalStorage("hamilton-api-key", undefined);

  if (username) {
    return (
      <UserContext.Provider
        value={{ username, setUsername, userAPIKey: apiKey }}
      >
        {props.children}
      </UserContext.Provider>
    );
  }

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setLocalUsername(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setUsername(localUsername); // Store username
  };

  const KeyInputExpandIcon = keyInputExpanded ? HiChevronUp : HiChevronDown;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 gap-2">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Welcome to the Hamilton UI!
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="flex flex-row items-center">
            <input
              type="text"
              autoComplete="username"
              name="username"
              value={username}
              onChange={handleChange}
              placeholder="Username"
              required
              className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-dwdarkblue focus:border-dwdarkblue focus:z-10 sm:text-sm"
            />
          </div>
          {keyInputExpanded && (
            <input
              type="password"
              autoComplete="api-key"
              name="api-key"
              value={apiKey || ""}
              onChange={(event) => {
                setApiKey(event.target.value);
              }}
              placeholder="API Key (power-user-mode)"
              required
              className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-dwdarkblue focus:border-dwdarkblue focus:z-10 sm:text-sm"
            />
          )}
          {/* <input
            type="text"
            autoComplete="username"
            name="username"
            value={username}
            onChange={handleChange}
            placeholder="Username"
            required
            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-dwdarkblue focus:border-dwdarkblue focus:z-10 sm:text-sm"
          /> */}
          <button
            type="submit"
            className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-dwdarkblue focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-dwdarkblue`}
          >
            <div className="flex flex-row justify-between w-full items-center">
              <div className="w-max">
                <span>Get started!</span>
              </div>
              <KeyInputExpandIcon
                onClick={() => setKeyInputExpanded(!keyInputExpanded)}
                className="h-6 w-6 text-white hover:scale-105"
              ></KeyInputExpandIcon>
            </div>
          </button>
        </form>
      </div>
    </div>
  );
};

export const localLogout = (redirectOnLogin: boolean) => {
  localStorage.removeItem("hamilton-username");
  localStorage.removeItem("hamilton-api-key");
  if (redirectOnLogin) {
    window.location.reload();
  }
};

export default LocalLoginProvider;
